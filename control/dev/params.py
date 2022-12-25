import json

# load the parameters from the json file
with open('params.json') as json_file:
    categories = json.load(json_file)
    # for all parameters, set values in environment
    for category in categories:
        # if categories[category] is not a string and it length is greater than 1
        if type(categories[category]) is not str and len(categories[category]) > 1:
            for param in categories[category]:
                # set the value of the parameter
                if type(categories[category][param]) is str:
                    exec(category + '_' + param + '="' + str(categories[category][param]) + '"')
                else:
                    exec(category + '_' + param + '=' + str(categories[category][param]))
        else:
            # set the value of the parameter
            if type(categories[category]) is str:
                exec(category + '="' + str(categories[category]) + '"')
            else:
                exec(category + '=' + categories[category])