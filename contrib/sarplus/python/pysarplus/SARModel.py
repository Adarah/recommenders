import logging
import pysarplus_cpp
import os
import gcsfs

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('sarplus')


class SARModel:
    __path = None
    __model = None

    def __init__(self, path):
        if SARModel.__model is not None and SARModel.__path == path:
            self.model = SARModel.__model
            return

        # find the .sar.related & .sar.offsets files
        if path.startswith("gs:"):
            fs = gcsfs.GCSFileSystem(project='maga-bigdata')
            sar_file = fs.glob(f'{path}/*.sar')[0]
            fs.get(sar_file, 'sarplus_cache.sar')
            all_files = './sarplus_cache.sar'
        else:
            # bad hack but oh well
            raise ValueError("Please use a gcs file.")

        #     all_files = os.listdir(path)

        # def find_or_raise(extension):
        #     files = [f for f in all_files if f.endswith(extension)]
        #     log.info(f"files are {files}")
        #     if len(files) != 1:
        #         raise ValueError(
        #             "Directory '%s' must contain exactly 1 file ending in '%s'"
        #             % (path, extension)
        #         )
        #     return path + "/" + files[0]
        def find_or_raise(extension):
            log.info(f"file is {all_files}")
            return all_files

        # instantiate C++ backend
        SARModel.__model = self.model = pysarplus_cpp.SARModelCpp(find_or_raise(".sar"))
        SARModel.__path = path

    def predict(self, items, ratings, top_k, remove_seen):
        return self.model.predict(items, ratings, top_k, remove_seen)
