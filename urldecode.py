from urllib.parse import unquote_plus

#decode the requested URL
def decode(param):
    param = param.replace('%E3', 'ã')
    param = param.replace('%E0', 'à')
    param = param.replace('%E1', 'á')
    param = param.replace('%E2', 'â')
    param = unquote_plus(param)
    return param
