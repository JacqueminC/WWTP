

class Evaluation:

    def __init__(self, note, info):
        if isinstance(note, int):
            if note <= 5:
                if note >=0:
                    self.note = note
                else:
                    raise Exception("La note ne doit pas être inférieur à 0 !")
            else:
                raise Exception("La note doit être inferieur à 5 !")  
        else:
             raise Exception("La valeur doit être un entier")

        if len(info.replace(" ","")) > 3:
            self.info = info
        else:
            raise Exception("Info doit contenir une valeur de 3 caractère minimum !")


