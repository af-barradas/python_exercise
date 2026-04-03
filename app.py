from services import report_service, mask_data_service


class DataProcesserApp:
    def __init__(self, source):
        self.source = source

    def run(self, config):
        data = self.source.read(config.INPUT_FILE)

        report_service.str_length_report(data, config.STRING_REPORT_COLUMNS)
        report_service.num_report(data, config.NUMERIC_REPORT_COLUMNS)
        mask_data_service.mask_values(data, config.MASK_COLUMNS)
        mask_data_service.calc_avg(data, config.AVG_COLUMNS)

        self.source.write(data, config.OUTPUT_FILE)
