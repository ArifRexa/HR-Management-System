from datetime import timedelta

from django.core.exceptions import BadRequest
from django.utils import timezone
from django_q.tasks import async_task
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from job_board.auth.CandidateAuth import CandidateAuth
from job_board.models.candidate import CandidateAssessment, CandidateJob
from job_board.serializers.assessment_serializer import GivenAssessmentAnswerSerializer, \
    CandidateAssessmentSerializer, AssessmentQuestionSerializer, AssessmentEvaluationUrlSerializer
from job_board.serializers.candidate_serializer import CandidateJobSerializer


class CandidateAssessmentBase(GenericAPIView):
    """
    This is base class for , Candidate Assessment List, Candidate Assessment Retrieve, And Start Exam
    """
    serializer_class = CandidateAssessmentSerializer
    authentication_classes = [CandidateAuth]
    lookup_field = 'unique_id'

    def get_queryset(self):
        user = self.request.user
        return CandidateAssessment.objects.filter(candidate_job__candidate=user).all()


class CandidateAssessmentList(CandidateAssessmentBase, mixins.ListModelMixin):
    """
    This class will return assessment list by authenticated user,
    You will need postman to submit with authorization header.

    To collect jwt auth token, visit [login](/api/login)
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CandidateJobRetrieve(GenericAPIView, mixins.RetrieveModelMixin):
    authentication_classes = [CandidateAuth]
    serializer_class = CandidateJobSerializer
    queryset = CandidateJob.objects.all()
    lookup_field = 'unique_id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CandidateAssessmentView(CandidateAssessmentBase, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    Candidate assessment view support get and put method
    get method just retrieve the assessment by given unique_id (which is a uuid4)

    put method is responsible to start the exam with following conditions
    if the exam is open_to_start and it's does not started yet
    if the exam is not open_to_start and candidate_assessment can_start_after is less then current date
    """
    authentication_classes = []

    def get_queryset(self):
        return CandidateAssessment.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        candidate_assessment = self.get_object()
        if candidate_assessment.assessment.open_to_start and candidate_assessment.exam_started_at is None:
            self._start_exam(candidate_assessment=candidate_assessment)
            return Response({'message': 'Exam started'})
        if candidate_assessment.can_start_after and \
                candidate_assessment.can_start_after <= timezone.now() and \
                candidate_assessment.exam_started_at is None:
            self._start_exam(candidate_assessment=candidate_assessment)
            return Response({'message': 'Exam Started'})

        msg = f'This assessment is not open to start, you can start exam after {candidate_assessment.can_start_after}'
        return Response({'admin_only': msg}, status=status.HTTP_403_FORBIDDEN)

    def _start_exam(self, candidate_assessment):
        candidate_assessment.exam_started_at = timezone.now()
        candidate_assessment.exam_end_at = timezone.now() + timedelta(
            minutes=candidate_assessment.assessment.duration)
        candidate_assessment.step = {
            'current_step': 0,
            'question_ids': list(
                candidate_assessment.assessment.assessmentquestion_set.values_list('id', flat=True)),
            'auto_checked': False
        }
        candidate_assessment.save()


class CandidateAssessmentQuestion(APIView):
    """
    Candidate Assessment Question only support get method
    it will lookup for candidate assessment by uuid and if the exam has started already
    it will return question serializer if have left step
    it will return time_up error if exam time up
    """

    def get(self, request, *args, **kwargs):
        """

        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        kwargs['exam_started_at__isnull'] = False
        try:
            candidate_assessment = CandidateAssessment.objects.filter(**kwargs).first()
            question_serializer = AssessmentQuestionSerializer(self.get_question(candidate_assessment))
            if not candidate_assessment.time_spend == 'time_up':
                return Response(question_serializer.data)
            return Response({'time_up': 'You have spend all the minutes ! best of luck'},
                            status=status.HTTP_400_BAD_REQUEST)
        except BadRequest:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    def get_question(self, candidate_assessment: CandidateAssessment):
        try:
            question_id = candidate_assessment.step['question_ids'][candidate_assessment.step['current_step']]
            return candidate_assessment.assessment.assessmentquestion_set.filter(id=question_id).first()
        except:
            raise serializers.ValidationError(
                {'out_of_step': f'You have answered all the question we have with {candidate_assessment.assessment}'})


class SaveAnswerView(GenericAPIView, mixins.CreateModelMixin):
    """
    Save answer question
    """
    serializer_class = GivenAssessmentAnswerSerializer

    # authentication_classes = [CandidateAuth]

    def post(self, request, *args, **kwargs):
        """
        save answer and return next question
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        self.create(request, *args, **kwargs)
        return Response({'answer_save': 'You given answer has been saved'})


class SaveEvaluationUrl(GenericAPIView):
    serializer_class = AssessmentEvaluationUrlSerializer

    def post(self, request, *args, **kwargs):
        serializer = AssessmentEvaluationUrlSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            candidate_assessment = CandidateAssessment.objects.filter(
                unique_id=validated_data['assessment_uuid'],
                assessment__open_to_start=False,
                exam_started_at__isnull=False,
                exam_end_at__gte=timezone.now()
            ).first()
            if candidate_assessment:
                candidate_assessment.evaluation_url = validated_data['evaluation_url']
                candidate_assessment.candidate_feedback = f"{timezone.now().date()} \n \n" \
                                                          f"{validated_data['candidate_feedback']} \n"
                candidate_assessment.exam_end_at = timezone.now()
                candidate_assessment.save()
                async_task('job_board.tasks.send_evaluation_url_to_admin', candidate_assessment)
                return Response({'success': 'Your evaluation url has been saved successfully.'
                                            ' We will review your submission very shortly'})
            return Response({'evaluation_url': 'We cannot save your evaluation url due some reason, '
                                               'The assessment_uuid might not found. '
                                               'Your exam time might expire'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
