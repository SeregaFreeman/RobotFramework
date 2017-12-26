from framework.support.Log import log_info
from test_project.api_call_builders.ColorsApi import ColorsApi
from test_project.models.ColorModel import ColorModel
from test_project.configurations.test_data import colors


def get_colors_model_from_file():
    colors_model = ColorModel(**colors)
    return colors_model


def get_color_from_api():
    return ColorsApi().get_colors()


def compare_colors(exp_color_model, act_color_model):
    log_info("Compare colors models. Exp : \n{exp_color_model} \nAct: \n{act_color_model}".format(
        exp_color_model=exp_color_model, act_color_model=act_color_model))
    assert exp_color_model.__eq__(act_color_model), "The ColorsModel are not equal. Exp = {expected}, Act = {actual}".\
        format(expected=exp_color_model, actual=act_color_model)
