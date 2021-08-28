from fpdf import FPDF

class PDF():
    def __init__(self,filename,funcion = " "):
        self.filename = filename
        self.funtion = funcion
    
    def makePDF(self):
        
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Times","B",13)
        pdf.image("espe.png",x=10,y=10,w=33,h=33)

        pdf.cell(0,15,"\t\t\t\tUNIVERSIDAD DE LAS FUERZAS ARMADAS ESPE",ln=1,align='C')
        pdf.cell(0,3,"\t\t\t\tCalculo Vectorial",ln=1,align='C')
        pdf.cell(0,15,"\t\t\t\tGraficador de Funiones",ln=1,align='C')


        #DATOS DE LA FUNCION
        pdf.set_font(size=13,family="Times",style="B")
        pdf.cell(0,15,"Función: " + self.funtion ,ln=1)

        #aqui va la imagen 

        #Curva de nivel
        


        pdf.output(self.filename + ".pdf")