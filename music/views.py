from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Score
from .serializers import ScoreSerializer


class ScoreListView(APIView):
    def get(self, request):
        try:
            rows_per_page = int(request.GET.get('rows_per_page', 10))
        except ValueError:
            rows_per_page = 10

        try:
            offset = int(request.query_params.get(
                "offset", 0)) * rows_per_page
        except ValueError:
            offset = 0

        order_by = request.query_params.get("order_by", "-num_correct")
        game_type = request.query_params.get("game", "note_id")
        if game_type not in ["note_id", "interval_ear_training"]:
            game_type = "note_id"

        if "percentage" in order_by or "num_attempted" in order_by or "name" in order_by:
            secondary_sort = "-num_correct" if "-" in order_by else "num_correct"
        else:
            secondary_sort = "-percentage" if "-" in order_by else "percentage"

        scores = Score.objects.filter(game_type=game_type)
        count = scores.count()
        results = scores.order_by(order_by, secondary_sort)[
            offset:offset + rows_per_page]
        serializer = ScoreSerializer(results, many=True)
        return Response({
            "count": count,
            "scores": serializer.data
        })
