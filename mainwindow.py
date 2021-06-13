from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsScene
from PySide2.QtCore import Slot
from PySide2.QtGui import QPen, QColor, QTransform
from ui_mainwindow import Ui_MainWindow
from particulas.particulas import Particulas
from particulas.particula import Particula
from pprint import pformat

class MainWindow(QMainWindow):
    def __init__(self):
        #Llama al constructor del QMainWindow
        super(MainWindow, self).__init__()
        self.particulas = Particulas()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.agregar_final_pushButton.clicked.connect(self.click_agregar_final)
        self.ui.agregar_inicio_pushButton.clicked.connect(self.click_agregar_inicio)
        self.ui.mostrar_pushButton.clicked.connect(self.click_mostrar)
        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)

        self.ui.mostrar_tabla_pushButton.clicked.connect(self.mostrar_tabla)
        self.ui.buscar_pushButton.clicked.connect(self.buscar_id)

        self.ui.dibujar_pushButton.clicked.connect(self.dibujar)
        self.ui.limpiar_pushButton.clicked.connect(self.limpiar)
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.ui.id_pushButton.clicked.connect(self.ordenar_id)
        self.ui.distancia_pushButton.clicked.connect(self.ordenar_distancia)
        self.ui.velocidad_pushButton.clicked.connect(self.ordenar_velocidad)

        self.ui.grafo_pushButton.clicked.connect(self.mostrar_grafo)
        self.ui.actionRecorridos.triggered.connect(self.recorridos)
        self.ui.actionPrim.triggered.connect(self.prim)

        self.grafo = False 

    @Slot()
    def prim(self):
        if not self.grafo or len(self.particulas) == 0:
            QMessageBox.critical(
                self,
                "No se puede dibujar",
                "Es necesario que se convierta a grafo antes de realizar un recorrido"
            )
        else:
            origen_x = int(self.ui.origenx_spinBox.text())
            origen_y = int(self.ui.origeny_spinBox.text())
            origen = (origen_x, origen_y)
            print(origen)
            if origen not in self.particulas.to_dict():
                QMessageBox.critical(
                self,
                "No se puede recorrer",
                "Las coordenadas del origen no corresponden a ningun nodo del grafo."
                )
            else:
                #Cambiar a ventana de dibujo
                self.ui.tabWidget.setCurrentIndex(2)
                self.dibujar()
                pen = QPen()
                pen.setWidth(2)
                color = QColor(255,0,0)
                pen.setColor(color)

                arbol_expansion = self.particulas.prim(origen)
                for arista in arbol_expansion:
                    origen = arista[1]
                    destino = arista[2]
                    self.scene.addLine(origen[0]+3, origen[1]+3, destino[0]+3, destino[1]+3, pen)


    @Slot()
    def recorridos(self):
        if not self.grafo or len(self.particulas) == 0:
            QMessageBox.critical(
                self,
                "No se puede recorrer",
                "Es necesario que se convierta a grafo antes de realizar un recorrido"
            )
        else:
            origen_x = int(self.ui.origenx_spinBox.text())
            origen_y = int(self.ui.origeny_spinBox.text())
            origen = (origen_x, origen_y)
            print(origen)
            if origen not in self.particulas.to_dict():
                QMessageBox.critical(
                self,
                "No se puede recorrer",
                "Las coordenadas del origen no corresponden a ningun nodo del grafo."
                )
            else:
                profundidad = self.particulas.recorrido_profundidad(origen)
                print("Profundidad: ")
                print(profundidad)
                amplitud = self.particulas.recorrido_amplitud(origen)
                print("Amplitud: ")
                print(amplitud)
                self.ui.salida.clear()
                self.ui.salida.insertPlainText("Origen: " + str(origen) + "\n\n")
                self.ui.salida.insertPlainText("Profundidad: \n")
                self.ui.salida.insertPlainText(profundidad)
                self.ui.salida.insertPlainText("\nAmplitud: \n")
                self.ui.salida.insertPlainText(amplitud)
    
    @Slot()
    def mostrar_grafo(self):
        self.ui.salida.clear()
        grafo = self.particulas.to_dict()
        formato = pformat(grafo, width=80, indent=1)
        self.ui.salida.insertPlainText(formato)
        self.grafo = True

    def crear_grafo(self):
        grafo = self.particulas.to_dict()
        
    def wheelEvent(self, event):
        if event.delta() > 0:
            self.ui.graphicsView.scale(1.2, 1.2)
        else:
            self.ui.graphicsView.scale(0.8, 0.8)

    @Slot()
    def ordenar_id(self):
        self.particulas.sort_by_id()
        self.click_mostrar()
    @Slot()
    def ordenar_distancia(self):
        self.particulas.sort_by_distancia()
        self.click_mostrar()
    @Slot()
    def ordenar_velocidad(self):
        self.particulas.sort_by_velocidad()
        self.click_mostrar()
        

    @Slot()
    def dibujar(self):
        pen = QPen()
        pen.setWidth(2)
        for particula in self.particulas:
            r = particula.red
            g = particula.green
            b = particula.blue

            color = QColor(r, g, b)
            pen.setColor(color)

            x_origen = particula.origen_x
            y_origen = particula.origen_y
            x_destin = particula.destino_x
            y_destin = particula.destino_y

            self.scene.addEllipse(x_origen, y_origen, 6, 6, pen)
            self.scene.addEllipse(x_destin, y_destin, 6, 6, pen)
            self.scene.addLine(x_origen+3, y_origen+3, x_destin+3, y_destin+3, pen)

    @Slot()
    def limpiar(self):
        self.scene.clear()
        self.ui.graphicsView.setTransform(QTransform())

    @Slot()
    def buscar_id(self):
        id = self.ui.id_lineEdit.text()
        encontrado = False
        for particula in self.particulas:
            print(particula)
            if id == str(particula.id):
                self.ui.table.clear()
                self.ui.table.setColumnCount(10)
                headers = ["Id", "Origen x", "Origen y", "Destino x", "Destino y",
                "Velocidad", "Red", "Green", "Blue", "Distancia"]
                self.ui.table.setHorizontalHeaderLabels(headers)
                self.ui.table.setRowCount(len(self.particulas))
                self.ui.table.setRowCount(1)
                 #   Construir
                id_widget = QTableWidgetItem(str(particula.id))
                origen_x_widget = QTableWidgetItem(str(particula.origen_x))
                origen_y_widget = QTableWidgetItem(str(particula.origen_y))
                destino_x_widget = QTableWidgetItem(str(particula.destino_x))
                destino_y_widget = QTableWidgetItem(str(particula.destino_y))
                velocidad_widget = QTableWidgetItem(str(particula.velocidad))
                red_widget = QTableWidgetItem(str(particula.red))
                green_widget = QTableWidgetItem(str(particula.green))
                blue_widget = QTableWidgetItem(str(particula.blue))
                distancia_widget = QTableWidgetItem(str(particula.distancia))
                #   Crear widgets
                print (particula.id)
                self.ui.table.setItem(0, 0, id_widget)
                self.ui.table.setItem(0, 1, origen_x_widget)
                self.ui.table.setItem(0, 2, origen_y_widget)
                self.ui.table.setItem(0, 3, destino_x_widget)
                self.ui.table.setItem(0, 4, destino_y_widget)
                self.ui.table.setItem(0, 5, velocidad_widget)
                self.ui.table.setItem(0, 6, red_widget)
                self.ui.table.setItem(0, 7, green_widget)
                self.ui.table.setItem(0, 8, blue_widget)
                self.ui.table.setItem(0, 9, distancia_widget)
                encontrado = True
                return
        if not encontrado:
            QMessageBox.warning(
                self,
                "Atencion",
                f'La particula con el id "{id}" no fue encontrada'
            )

    @Slot()
    def mostrar_tabla(self):
        self.ui.table.setColumnCount(10)
        headers = ["Id", "Origen x", "Origen y", "Destino x", "Destino y",
        "Velocidad", "Red", "Green", "Blue", "Distancia"]
        self.ui.table.setHorizontalHeaderLabels(headers)
        self.ui.table.setRowCount(len(self.particulas))
        row = 0
        for particula in self.particulas:
            #   Construir
            id_widget = QTableWidgetItem(str(particula.id))
            origen_x_widget = QTableWidgetItem(str(particula.origen_x))
            origen_y_widget = QTableWidgetItem(str(particula.origen_y))
            destino_x_widget = QTableWidgetItem(str(particula.destino_x))
            destino_y_widget = QTableWidgetItem(str(particula.destino_y))
            velocidad_widget = QTableWidgetItem(str(particula.velocidad))
            red_widget = QTableWidgetItem(str(particula.red))
            green_widget = QTableWidgetItem(str(particula.green))
            blue_widget = QTableWidgetItem(str(particula.blue))
            distancia_widget = QTableWidgetItem(str(particula.distancia))
            #   Crear widgets
            print (particula.id)
            self.ui.table.setItem(row, 0, id_widget)
            self.ui.table.setItem(row, 1, origen_x_widget)
            self.ui.table.setItem(row, 2, origen_y_widget)
            self.ui.table.setItem(row, 3, destino_x_widget)
            self.ui.table.setItem(row, 4, destino_y_widget)
            self.ui.table.setItem(row, 5, velocidad_widget)
            self.ui.table.setItem(row, 6, red_widget)
            self.ui.table.setItem(row, 7, green_widget)
            self.ui.table.setItem(row, 8, blue_widget)
            self.ui.table.setItem(row, 9, distancia_widget)
            row += 1

    @Slot()
    def action_abrir_archivo(self):
        # print('Abrir archivo')
        ubicacion = QFileDialog.getOpenFileName(
            self,
            'Abrir Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        if self.particulas.abrir(ubicacion):
            QMessageBox.information(
                self,
                "Éxito",
                "Se abrió el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + ubicacion
            )
    
    @Slot()
    def action_guardar_archivo(self):
        # print('Guardar archivo')
        ubicacion = QFileDialog.getSaveFileName(
            self,   #Se lanza desde esta ventana
            'Guardar archivo',  #Titulo
            '.',    #Direccion
            'JSON (*.json)' #Formato
        )[0]
        print(ubicacion)
        if self.particulas.guardar(ubicacion):
            QMessageBox.information(
                self,
                "Exito",
                "Se pudo crear el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo " + ubicacion
            )

    @Slot()
    def click_agregar_final(self):
        id = self.ui.id_spinBox.value()
        origenx = self.ui.origenx_spinBox.value()
        origeny = self.ui.origeny_spinBox.value()
        destinox = self.ui.destinox_spinBox.value()
        destinoy = self.ui.destinoy_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        red = self.ui.red_spinBox.value()
        green = self.ui.green_spinBox.value()
        blue = self.ui.blue_spinBox.value()
        particula = Particula(id, origenx, origeny, destinox, destinoy, velocidad, red, green, blue)
        self.particulas.agregarFinal(particula)
    @Slot()
    def click_agregar_inicio(self):
        id = self.ui.id_spinBox.value()
        origenx = self.ui.origenx_spinBox.value()
        origeny = self.ui.origeny_spinBox.value()
        destinox = self.ui.destinox_spinBox.value()
        destinoy = self.ui.destinoy_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        red = self.ui.red_spinBox.value()
        green = self.ui.green_spinBox.value()
        blue = self.ui.blue_spinBox.value()
        particula = Particula(id, origenx, origeny, destinox, destinoy, velocidad, red, green, blue)
        self.particulas.agregarInicio(particula) 
    @Slot()
    def click_mostrar(self):
        self.ui.salida.clear()
        self.ui.salida.insertPlainText(str(self.particulas))
