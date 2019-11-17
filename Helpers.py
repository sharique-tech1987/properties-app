class Helpers:
    @staticmethod
    def PopulateModel(request, property_params_list, additional_params={}):
        model = {}
        for key, value in additional_params.items():
            model[key] = value
        for key_name in property_params_list:
            model[key_name] = request.json[key_name]
            
        return model