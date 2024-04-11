from jkfennerai.inference import predict
import traceback

class LoadJKFennerModel():

   predictor = None
   config_file_path = ""

   def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(LoadJKFennerModel, cls).__new__(cls)
    return cls.instance

   def __init__(self):
      if self.predictor is None:
         try:
            self.predictor = predict("/home/mazeworks/frappe-bench-lms/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig.cfg")
         except Exception as error:
            print(traceback.format_exc())
