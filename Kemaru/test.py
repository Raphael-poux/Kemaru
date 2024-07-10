def string_conversion(string):
    text = string.split('_')
    liste = [[0]]
    n = len(text)
    for i in range(n):
        if len(text[i]) == 1 and liste[-1][0] == 1 :
            liste.append([0])
            pass
        elif len(text[i]) > 1 and liste[-1][0] == 0:
            liste.append([int(text[i].split('-')[0]), (int(text[i].split('-')[1]), int(text[i].split('-')[2]))])
            liste.append([0])
    if liste[-1][0] != 0:
        liste.append([0])
    return liste

print(string_conversion('0_1-2-3_0_1-5-4'))
