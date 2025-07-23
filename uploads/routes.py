from flask import send_from_directory
from flask_restx import Resource

UPLOAD_FOLDER = 'uploads/potholes'

class PotholeImages():
  @staticmethod
  def init(ns):
    @ns.route('/potholes/<filename>')
    class PotholeImagesRoute(Resource):
      def get(self, filename):
          return send_from_directory(UPLOAD_FOLDER, filename)
      
def init_uploads_routes(api, schemas):
  """Uploads 라우트 초기화"""
  #init_uploads_schemas(schemas)
  
  # Uploads 네임스페이스 생성
  uploads_ns = api.namespace('uploads', description='Uploads 관련 API')
  
  # 라우트 등록
  PotholeImages.init(uploads_ns)