#########################
##                     ##
## Irving Gomez Mendez ##
##  October 17, 2021   ##
##                     ##
#########################

import numpy as np
import readline
import matplotlib.animation as anim
import matplotlib.pyplot as plt

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()

class juego_canicas:
    def __init__(self, canicas_ali, canicas_sang, numero_juegos, aleatorio, jugador_inicial = None):
        self.canicas_ali = canicas_ali
        self.canicas_sang = canicas_sang
        self.numero_juegos = numero_juegos
        self.aleatorio = aleatorio
        self.jugador_inicial = jugador_inicial

    def jugar_canicas(self):
        canicas = dict({'Ali': self.canicas_ali, 'Sangwoo': self.canicas_sang})
        mano = dict({'Ali': 0, 'Sangwoo': 0})

        if self.aleatorio:
            turno = np.random.choice(['Ali', 'Sangwoo'])
            jugamos = True
        else:
            turno = self.jugador_inicial
            jugamos = True

        while jugamos:
            otro = np.array_str(np.where(turno == 'Ali', 'Sangwoo', 'Ali'))

            mano['Ali'] = np.random.choice(np.arange(canicas['Ali'])+1)
            mano['Sangwoo'] = np.random.choice(np.arange(canicas['Sangwoo'])+1)

            apuesta = np.random.choice(range(2))

            if (mano[otro] % 2) == apuesta:
                canicas[turno] += mano[turno]
                canicas[otro] -= mano[turno]
                if canicas[turno] >= self.canicas_ali + self.canicas_sang:
                    return(turno)
            else:
                canicas[turno] -= mano[otro]
                canicas[otro] += mano[otro]
                if canicas[turno] <= 0:
                    return(otro)

            turno = np.array_str(np.where(turno == 'Ali', 'Sangwoo', 'Ali'))

    def grafica(self):
        vec_ganados_avg = []
        vec_ganados_abs = []
        juegos_ganados_ali = 0

        for i in range(self.numero_juegos):
            ganador = self.jugar_canicas()
            if ganador == 'Ali':
                juegos_ganados_ali += 1
            vec_ganados_avg.append(juegos_ganados_ali/(i+1))
            vec_ganados_abs.append(juegos_ganados_ali)

        def build_bar(i):
            ax1.bar([0,1],
            [vec_ganados_abs[i], i+1-vec_ganados_abs[i]],
            color=['DodgerBlue', 'DeepPink'])
            ax1.set_title('Juegos jugados: ' + str(i+1))
            ax1.set_ylabel('Juegos ganados')
            ax1.set_xticks([0,1])
            ax1.set_xticklabels(['Alí', 'Sangwoo'])

        def build_series(i):
            ax2.plot(np.arange(i)+1,vec_ganados_avg[:i], color = 'RebeccaPurple', lw = 0.5)
            ax2.axhline(y = 0.5, color = 'r', linestyle = '--')
            ax2.set_xlabel('Juegos jugados')
            ax2.set_ylabel('Proporción de juegos ganados por Alí')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (15,7.5))

        a = anim.FuncAnimation(fig,
            build_bar,
            frames = self.numero_juegos,
            repeat = False,
            interval = 100)

        b = anim.FuncAnimation(fig,
            build_series,
            frames = self.numero_juegos,
            repeat = False,
            interval = 100)

        plt.show()

class costants:
    def __init__(self):
        input("\nLa mayor parte de este programa está basado en el codigo de Rafael Gonzalez-Gouveia." \
            + " Mi aportacion se limita a escribirlo con clases, realizar el gráfico de barras, que pueda ser jugado a través de la terminal y agregar la opcion de seleccionar al jugador inicial.\n\n" \
            + "Irving Gomez-Mendez\n\n\n"
        )
        self.canicas_ali = int(rlinput("Numero de canicas que tiene Ali: ", '10'))
        self.canicas_sang = int(rlinput("Numero de canicas que tiene Sangwoo: ", '10'))
        self.numero_juegos = int(rlinput("Numero de juegos a jugar: ", '300'))
        self.jugador_inicial = rlinput("Jugador inicial (Aleatorio, Ali, Sangwoo): ", 'Ali')
        self.aleatorio = False
        if self.jugador_inicial == 'Aleatorio': self.aleatorio = True

def main():
    CONSTANTS = costants()
    juego = juego_canicas(CONSTANTS.canicas_ali, CONSTANTS.canicas_sang, CONSTANTS.numero_juegos, CONSTANTS.aleatorio, CONSTANTS.jugador_inicial)
    juego.grafica()

if __name__ == "__main__":
      main()

###
