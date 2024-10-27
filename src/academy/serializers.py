from rest_framework import serializers

from academy.models import (
    MarketingSlider,
    Training,
    TrainingLearningTopic,
    TrainingOutline,
    TrainingProject,
    TrainingStructure,
    TrainingStructureModule,
    TrainingTechnology,
)
from website.serializers import TechnologySerializer


class MarketingSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingSlider
        fields = "__all__"


class TrainingStructureModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingStructureModule
        fields = [
            "day",
            "description",
        ]


class TrainingStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingStructure
        fields = [
            "week",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["days"] = TrainingStructureModuleSerializer(
            instance=instance.training_modules.filter(
                training=self.context.get("training"), training_structure=instance
            ),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        return data


class TrainingOutlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingOutline
        fields = [
            "title",
            "description",
            "image",
        ]


class TrainingTechnologySerializer(serializers.ModelSerializer):
    technology_name = TechnologySerializer(many=True)

    class Meta:
        model = TrainingTechnology
        fields = [
            "title",
            "technology_name",
        ]


class TrainingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProject
        fields = [
            "image",
        ]


class TrainingLearningTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingLearningTopic
        fields = [
            "title",
            "icon",
        ]


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ["id", "title", "description", "video", "duration", "image"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        structure = TrainingStructure.objects.filter(
            training_modules__training__id=instance.id
        ).distinct()
        data["training_structure"] = TrainingStructureSerializer(
            instance=structure,
            many=True,
            context={"request": self.context.get("request"), "training": instance},
        ).data
        data["training_outline"] = TrainingOutlineSerializer(
            instance=instance.training_outlines.all(),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        data["training_project"] = TrainingProjectSerializer(
            instance=instance.training_projects.all(),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        data["learning_topic"] = TrainingLearningTopicSerializer(
            instance=instance.training_learning_topics.all(),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        data["technology"] = TrainingTechnologySerializer(
            instance=instance.training_technologies.all(),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        return data


class TrainingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = [
            "id",
            "title",
            "description",
            "image",
            "duration",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["technology"] = TrainingTechnologySerializer(
            instance=instance.training_technologies.all(),
            many=True,
            context={"request": self.context.get("request")},
        ).data
        return data