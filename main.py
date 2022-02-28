from decimal import Decimal, Overflow
import math
from PyQt5.QtWidgets import QApplication,QMainWindow 
from PyQt5.QtGui import QIcon 
import sys
from PyQt5 import  uic
import os
from functools import partial
rootPath = os.path.dirname(os.path.abspath(__file__))



class main(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(rootPath,"main.ui"),self)
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(350,500)  
        self.state()
        self.Display.setReadOnly(True)
        self.OperationViewer.setReadOnly(True)
        self.btn0.clicked.connect(partial(self.btnNumber_Click,self.btn0.text()))
        self.btn1.clicked.connect(partial(self.btnNumber_Click,self.btn1.text()))
        self.btn2.clicked.connect(partial(self.btnNumber_Click,self.btn2.text()))
        self.btn3.clicked.connect(partial(self.btnNumber_Click,self.btn3.text()))
        self.btn4.clicked.connect(partial(self.btnNumber_Click,self.btn4.text()))
        self.btn5.clicked.connect(partial(self.btnNumber_Click,self.btn5.text()))
        self.btn6.clicked.connect(partial(self.btnNumber_Click,self.btn6.text()))
        self.btn7.clicked.connect(partial(self.btnNumber_Click,self.btn7.text()))
        self.btn8.clicked.connect(partial(self.btnNumber_Click,self.btn8.text()))
        self.btn9.clicked.connect(partial(self.btnNumber_Click,self.btn9.text()))
        self.btnPlus.clicked.connect(partial(self.btnOperator_Click,self.btnPlus.text()))
        self.btnNegative.clicked.connect(partial(self.btnOperator_Click,self.btnNegative.text()))
        self.btnMultiply.clicked.connect(partial(self.btnOperator_Click,self.btnMultiply.text()))
        self.btnDivision.clicked.connect(partial(self.btnOperator_Click,self.btnDivision.text()))
        self.btnX2.clicked.connect(self.btnX2_Click)
        self.btnDot.clicked.connect(self.btnDot_Click)
        self.btnEqual.clicked.connect(self.btnEqual_Click)
        self.btnDelete.clicked.connect(self.btnDelete_Click)
        self.btnPlus_Negative.clicked.connect(self.btnPlus_Negative_Click)
        self.btnCE.clicked.connect(self.btnCE_Click)
        self.btnC.clicked.connect(self.btnC_Click)
        self.btnRadical.clicked.connect(self.btnRadical_Click)
        self.btn1Dx.clicked.connect(self.btn1Dx_Click)
        self.btnPercent.clicked.connect(self.btnPercent_Click)
        

    def state(self):
        self.isLastCharterOperator = False 
        self.isLastCharterEqual = False     
        self.isLastCharterPowerOrRadical = False     
        self.getDispalyText:function = self.Display.text
        self.getOperationViewerText:function = self.OperationViewer.text
        self.setDispalyText:function = self.Display.setText
        self.setOperationViewerText:function = self.OperationViewer.setText
        self.clearOperationViewerText:function = self.OperationViewer.clear
        
    def btnNumber_Click(self,value):
        if(self.getOperationViewerText() == "ERROR"):return
        text = self.getDispalyText()
        if(len(text) >= 13 or self.isLastCharterPowerOrRadical) :return 
        if(self.isLastCharterEqual):  self.resetCalculator()
        if(text == "0" or self.isLastCharterOperator or self.isLastCharterEqual) : self.setDispalyText(value)
        else : self.setDispalyText(text+value)
        self.isLastCharterOperator = False 
        self.isLastCharterEqual = False 
        
    def btnOperator_Click (self,value):
        if(self.getOperationViewerText() == "ERROR"):return
        textDisplay = self.Display.text()
        textOperationViewer =  self.getOperationViewerText()
        if(self.isLastCharterOperator) : return self.setOperationViewerText( textOperationViewer[:-1] + value )
        if(self.isLastCharterEqual): 
            self.setOperationViewerText( textDisplay + value )
        elif(self.isLastCharterPowerOrRadical): self.setOperationViewerText(textOperationViewer + value )
        else : 
            self.setOperationViewerText(textOperationViewer + textDisplay + value)
            self.setDispalyText(calculates(textOperationViewer+textDisplay))
        self.isLastCharterOperator = True 
        self.isLastCharterEqual = False 
        self.isLastCharterPowerOrRadical = False 

    def btnPlus_Negative_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        textDisplay:str = self.Display.text()
        if (textDisplay == "0") : return
        if("-" in textDisplay ): self.setDispalyText(textDisplay[1:])  
        else : self.setDispalyText("-"+textDisplay)

    def btnEqual_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        if(self.isLastCharterEqual): return
        textDisplay = self.Display.text()
        textOperationViewer =  self.getOperationViewerText()
        combine:str = textOperationViewer+textDisplay
        textOperationViewer= self.getOperationViewerText()
        self.setOperationViewerText(textOperationViewer+textDisplay+"=")
        self.setDispalyText(calculates(combine))
        self.isLastCharterEqual = True
        self.isLastCharterOperator = False 
        self.isLastCharterPowerOrRadical=False
    def btnCE_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        self.setDispalyText("0")
        if(self.isLastCharterEqual) : self.resetCalculator()
        self.isLastCharterEqual = False
        self.isLastCharterOperator = False   
      
    def btnC_Click(self):
        self.setDispalyText("0")
        self.OperationViewer.clear()
        self.isLastCharterOperator = False 
        self.isLastCharterEqual = False
        self.isLastCharterPowerOrRadical = False

    def btnDelete_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        textDisplay = self.Display.text()
        if(len(textDisplay) == 1): self.setDispalyText("0")
        else : self.setDispalyText(textDisplay[:-1])

    def btnDot_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        textDisplay:str = self.Display.text()
        if(self.isLastCharterEqual) :self.resetCalculator()
        if("." in textDisplay and not( self.isLastCharterOperator or self.isLastCharterEqual)) : return
        if(textDisplay=="0" or self.isLastCharterOperator or self.isLastCharterEqual) :self.setDispalyText("0.")
        else : self.setDispalyText(textDisplay +".")
        self.isLastCharterOperator =False
        self.isLastCharterEqual =False

    def resetCalculator(self):
        self.clearOperationViewerText()
        self.setDispalyText("0")
    
    def btnX2_Click (self):
        if(self.getOperationViewerText() == "ERROR"):return
        DispalyText =self.getDispalyText()
        OperationViewerText =self.getOperationViewerText()
        if(self.isLastCharterPowerOrRadical): self.setOperationViewerText(OperationViewerText+"²")
        elif(self.isLastCharterEqual): self.setOperationViewerText(DispalyText+"²")
        else:self.setOperationViewerText(OperationViewerText+DispalyText+"²")
        self.setDispalyText(calculates(self.getOperationViewerText()))
        self.isLastCharterPowerOrRadical=True
        self.isLastCharterEqual=False

    def btnRadical_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        DispalyText =self.getDispalyText()
        OperationViewerText =self.getOperationViewerText()
        if(self.isLastCharterPowerOrRadical): self.setOperationViewerText("√"+"("+OperationViewerText+")")
        elif(self.isLastCharterEqual): self.setOperationViewerText("√"+"(" + DispalyText + ")")
        else:self.setOperationViewerText(OperationViewerText+"√"+"("+DispalyText+")")
        self.setDispalyText(calculates(self.getOperationViewerText()))
        self.isLastCharterPowerOrRadical=True
        self.isLastCharterEqual=False 
    
    def btn1Dx_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        DispalyText =self.getDispalyText()
        OperationViewerText =self.getOperationViewerText()
        if(self.isLastCharterPowerOrRadical): self.setOperationViewerText("1/"+"("+OperationViewerText+")")
        elif(self.isLastCharterEqual): self.setOperationViewerText("1/"+"(" + DispalyText + ")")
        else:self.setOperationViewerText(OperationViewerText+"1/"+"("+DispalyText+")")
        self.setDispalyText(calculates(self.getOperationViewerText()))
        self.isLastCharterPowerOrRadical=True
        self.isLastCharterEqual=False 

    def btnPercent_Click(self):
        if(self.getOperationViewerText() == "ERROR"):return
        DispalyText =self.getDispalyText()
        OperationViewerText =self.getOperationViewerText()
        if(self.isLastCharterPowerOrRadical): self.setOperationViewerText("("+OperationViewerText+")"+"%")
        elif(self.isLastCharterEqual): self.setOperationViewerText("(" + DispalyText + ")"+"%")
        else:self.setOperationViewerText(OperationViewerText+"("+DispalyText+")"+"%")
        self.setDispalyText(calculates(self.getOperationViewerText()))
        self.isLastCharterPowerOrRadical=True
        self.isLastCharterEqual=False      

def calculates(value:str):
    if(window.getDispalyText() == "ERROR" or window.getDispalyText() == "OVERFLOW") :return
    value = value.replace("×","*")
    value = value.replace("÷","/")
    value = value.replace("²","**2")
    value = value.replace("√","math.sqrt")
    value = value.replace("%","*1/100")
    try:
        isOverFlow = eval(value) >= (2**32)
        
        if(isOverFlow) : 
            window.setOperationViewerText("ERROR") 
            return "OVERFLOW"
        else :
            value = eval(value)
            lenValue = len(str(value))
            if(value <= 10**6 and value>=10**-6): 
                if(lenValue < 12): 
                    return str(value)
                else :
                    return str(Decimal(value))[0:12]
            else :
                locationE = str(value).find("e")
                if(lenValue < 12): 
                    return str(value)
                else :
                    if(locationE != -1):
                        return str(Decimal(value))[0:12] + str(Decimal(value))[locationE-lenValue:]
                    else : 
                        return str(Decimal(value))[0:12]              
    except:
       window.setOperationViewerText("ERROR") 
       return "ERROR"

app = QApplication(sys.argv)
window = main()
window.show()
app.exec_()


