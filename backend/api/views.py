from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DataSet
from .serializers import DataSetSerializer
import pandas as pd
from rest_framework.decorators import action
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import io
from rest_framework.permissions import AllowAny, IsAuthenticated

class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve', 'data', 'generate_report']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        file_obj = request.data.get('file')
        if not file_obj:
            return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file_obj)
            
            summary = {
                'total_count': len(df),
                'averages': {
                    'Flowrate': df['Flowrate'].mean(),
                    'Pressure': df['Pressure'].mean(),
                    'Temperature': df['Temperature'].mean(),
                },
                'type_distribution': df['Type'].value_counts().to_dict()
            }

            dataset = DataSet.objects.create(
                name=file_obj.name,
                file=file_obj,
                summary=summary
            )

            all_datasets = DataSet.objects.all()
            if all_datasets.count() > 5:
                oldest_dataset = all_datasets.last()
                if oldest_dataset.file:
                    oldest_dataset.file.delete(save=False)
                oldest_dataset.delete()
            
            serializer = self.get_serializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def data(self, request):
        dataset_id = request.query_params.get('id')
        if not dataset_id:
            return Response({'error': 'Dataset ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        dataset = get_object_or_404(DataSet, pk=dataset_id)
        try:
            with dataset.file.open('rb') as f:
                df = pd.read_csv(f)
                return Response(df.to_dict('records'))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def generate_report(self, request):
        dataset_id = request.query_params.get('id')
        if not dataset_id:
            return Response({'error': 'Dataset ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        dataset = get_object_or_404(DataSet, pk=dataset_id)
        summary = dataset.summary

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.name}_report.pdf"'

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        p.setFont("Helvetica-Bold", 16)
        p.drawString(1 * inch, 10 * inch, f"Analysis Report for: {dataset.name}")

        p.setFont("Helvetica", 12)
        p.drawString(1 * inch, 9.5 * inch, "Summary Statistics:")
        p.drawString(1.2 * inch, 9.2 * inch, f"Total Equipment Count: {summary['total_count']}")
        
        p.drawString(1.2 * inch, 9.0 * inch, "Averages:")
        p.drawString(1.4 * inch, 8.8 * inch, f"Flowrate: {summary['averages']['Flowrate']:.2f}")
        p.drawString(1.4 * inch, 8.6 * inch, f"Pressure: {summary['averages']['Pressure']:.2f}")
        p.drawString(1.4 * inch, 8.4 * inch, f"Temperature: {summary['averages']['Temperature']:.2f}")

        type_dist = summary['type_distribution']
        labels = type_dist.keys()
        sizes = type_dist.values()

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title('Equipment Type Distribution')

        from reportlab.lib.utils import ImageReader

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close(fig)
        img_buffer.seek(0)
        
        # Wrap the buffer in ImageReader
        image = ImageReader(img_buffer)
        p.drawImage(image, 1 * inch, 4 * inch, width=4*inch, height=3*inch)

        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def get_queryset(self):
        return DataSet.objects.all()[:5]

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)