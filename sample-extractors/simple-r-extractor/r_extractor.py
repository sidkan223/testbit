#!/usr/bin/env python

import json
import logging
import os

from pyclowder.extractors import Extractor
import pyclowder.files
import rpy2.robjects as robjects

r_script = os.getenv("R_SCRIPT")
r_function = os.getenv("R_FUNCTION")


class RExtractor(Extractor):
    def __init__(self):
        Extractor.__init__(self)
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.INFO)
        self.logger = logging.getLogger('__main__')
        self.logger.setLevel(logging.INFO)

    def process_message(self, connector, host, secret_key, resource, parameters):
        input_file = resource["local_paths"][0]
        file_id = resource['id']

        r_result = robjects.r('''
            source("%s")
            result <- do.call("%s", list("%s"))
            jsonlite::toJSON(result, auto_unbox=TRUE)
        ''' % (r_script, r_function, input_file))
        result = json.loads(str(r_result))

        if 'metadata' in result.keys():
            metadata = self.get_metadata(result.get('metadata'), 'file', file_id, host)
            self.logger.info("upload metadata")
            self.logger.debug(metadata)
            pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)
        if 'previews' in result.keys():
            self.logger.info("upload previews")
            for preview in result['previews']:
                if isinstance(preview, basestring):
                    preview = {'file': preview}
                else:
                    continue
                self.logger.info("upload preview")
                pyclowder.files.upload_preview(connector, host, secret_key, file_id, preview.get('file'),
                                               preview.get('metadata'), preview.get('mimetype'))


RExtractor().start()
