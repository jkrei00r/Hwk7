# Complete imports
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QGroupBox,
                            QLabel, QVBoxLayout, QComboBox, QLineEdit,
                            QPushButton, QRadioButton)
from PyQt5.QtCore import Qt
from pyXSteam.XSteam import XSteam
from UnitConversion import UC
from scipy.optimize import fsolve
import sys

# endregion

class ThermoCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.initUI()

        # Set default units to SI
        self.currentUnits = 'SI'
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

        # Connect signals
        self.connectSignals()

        # Set initial units
        self.setUnits()

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle('Thermodynamic State Calculator')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        mainLayout = QVBoxLayout()

        # Units selection
        self.unitGroup = QGroupBox('System of Units')
        unitLayout = QHBoxLayout()
        self.siRadio = QRadioButton('SI')
        self.siRadio.setChecked(True)
        self.engRadio = QRadioButton('English')
        unitLayout.addWidget(self.siRadio)
        unitLayout.addWidget(self.engRadio)
        self.unitGroup.setLayout(unitLayout)
        mainLayout.addWidget(self.unitGroup)

        # State input section
        self.stateGroup = QGroupBox('Specified Properties')
        stateLayout = QHBoxLayout()

        # State 1
        self.state1Group = QGroupBox('State 1')
        state1Layout = QVBoxLayout()

        # Property 1
        self.prop1Label1 = QLabel('Property 1:')
        self.prop1Combo1 = QComboBox()
        self.prop1Combo1.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                                   'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                                   'Specific Volume (v)', 'Specific Entropy (s)'])
        self.prop1Value1 = QLineEdit('1.0')
        self.prop1Unit1 = QLabel('bar')

        # Property 2
        self.prop2Label1 = QLabel('Property 2:')
        self.prop2Combo1 = QComboBox()
        self.prop2Combo1.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                                   'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                                   'Specific Volume (v)', 'Specific Entropy (s)'])
        self.prop2Combo1.setCurrentIndex(1)  # Default to Temperature
        self.prop2Value1 = QLineEdit('100.0')
        self.prop2Unit1 = QLabel('C')

        # Add to state 1 layout
        state1Layout.addWidget(self.prop1Label1)
        state1Layout.addWidget(self.prop1Combo1)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.prop1Value1)
        hbox1.addWidget(self.prop1Unit1)
        state1Layout.addLayout(hbox1)

        state1Layout.addWidget(self.prop2Label1)
        state1Layout.addWidget(self.prop2Combo1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.prop2Value1)
        hbox2.addWidget(self.prop2Unit1)
        state1Layout.addLayout(hbox2)

        self.state1Group.setLayout(state1Layout)

        # State 2
        self.state2Group = QGroupBox('State 2')
        state2Layout = QVBoxLayout()

        # Property 1
        self.prop1Label2 = QLabel('Property 1:')
        self.prop1Combo2 = QComboBox()
        self.prop1Combo2.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                                   'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                                   'Specific Volume (v)', 'Specific Entropy (s)'])
        self.prop1Value2 = QLineEdit('1.0')
        self.prop1Unit2 = QLabel('bar')

        # Property 2
        self.prop2Label2 = QLabel('Property 2:')
        self.prop2Combo2 = QComboBox()
        self.prop2Combo2.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                                   'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                                   'Specific Volume (v)', 'Specific Entropy (s)'])
        self.prop2Combo2.setCurrentIndex(1)  # Default to Temperature
        self.prop2Value2 = QLineEdit('100.0')
        self.prop2Unit2 = QLabel('C')

        # Add to state 2 layout
        state2Layout.addWidget(self.prop1Label2)
        state2Layout.addWidget(self.prop1Combo2)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.prop1Value2)
        hbox3.addWidget(self.prop1Unit2)
        state2Layout.addLayout(hbox3)

        state2Layout.addWidget(self.prop2Label2)
        state2Layout.addWidget(self.prop2Combo2)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.prop2Value2)
        hbox4.addWidget(self.prop2Unit2)
        state2Layout.addLayout(hbox4)

        self.state2Group.setLayout(state2Layout)

        # Add states to main state layout
        stateLayout.addWidget(self.state1Group)
        stateLayout.addWidget(self.state2Group)
        self.stateGroup.setLayout(stateLayout)
        mainLayout.addWidget(self.stateGroup)

        # Calculate button
        self.calcButton = QPushButton('Calculate')
        mainLayout.addWidget(self.calcButton)

        # Results section
        self.resultsGroup = QGroupBox('State Properties')
        resultsLayout = QHBoxLayout()

        # State 1 results
        self.state1Results = QGroupBox('State 1 Properties')
        self.state1Text = QLabel('Properties will be shown here')
        state1ResLayout = QVBoxLayout()
        state1ResLayout.addWidget(self.state1Text)
        self.state1Results.setLayout(state1ResLayout)

        # State 2 results
        self.state2Results = QGroupBox('State 2 Properties')
        self.state2Text = QLabel('Properties will be shown here')
        state2ResLayout = QVBoxLayout()
        state2ResLayout.addWidget(self.state2Text)
        self.state2Results.setLayout(state2ResLayout)

        # Delta results
        self.deltaResults = QGroupBox('Property Changes (2-1)')
        self.deltaText = QLabel('Changes will be shown here')
        deltaResLayout = QVBoxLayout()
        deltaResLayout.addWidget(self.deltaText)
        self.deltaResults.setLayout(deltaResLayout)

        # Add to results layout
        resultsLayout.addWidget(self.state1Results)
        resultsLayout.addWidget(self.state2Results)
        resultsLayout.addWidget(self.deltaResults)
        self.resultsGroup.setLayout(resultsLayout)
        mainLayout.addWidget(self.resultsGroup)

        # Set main layout
        self.setLayout(mainLayout)

    def connectSignals(self):
        """Connect all signals to their slots"""
        self.siRadio.toggled.connect(self.setUnits)
        self.prop1Combo1.currentIndexChanged.connect(self.setUnits)
        self.prop2Combo1.currentIndexChanged.connect(self.setUnits)
        self.prop1Combo2.currentIndexChanged.connect(self.setUnits)
        self.prop2Combo2.currentIndexChanged.connect(self.setUnits)
        self.calcButton.clicked.connect(self.calculate)

    def setUnits(self):
        """Set the units based on current selection"""
        SI = self.siRadio.isChecked()
        self.currentUnits = 'SI' if SI else 'EN'

        if SI:
            self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
            self.p_Units = "bar"
            self.t_Units = "C"
            self.u_Units = "kJ/kg"
            self.h_Units = "kJ/kg"
            self.s_Units = "kJ/kg*C"
            self.v_Units = "m^3/kg"
        else:
            self.steamTable = XSteam(XSteam.UNIT_SYSTEM_FLS)
            self.p_Units = "psi"
            self.t_Units = "F"
            self.u_Units = "btu/lb"
            self.h_Units = "btu/lb"
            self.s_Units = "btu/lb*F"
            self.v_Units = "ft^3/lb"

        # Update unit labels
        self.updateUnitLabels()

    def updateUnitLabels(self):
        """Update all unit labels based on current units"""
        # State 1
        self.updatePropertyUnits(self.prop1Combo1, self.prop1Value1, self.prop1Unit1)
        self.updatePropertyUnits(self.prop2Combo1, self.prop2Value1, self.prop2Unit1)

        # State 2
        self.updatePropertyUnits(self.prop1Combo2, self.prop1Value2, self.prop1Unit2)
        self.updatePropertyUnits(self.prop2Combo2, self.prop2Value2, self.prop2Unit2)

    def updatePropertyUnits(self, combo, valueEdit, unitLabel):
        """Update units for a single property"""
        prop = combo.currentText()

        if 'Pressure' in prop:
            unitLabel.setText(self.p_Units)
        elif 'Temperature' in prop:
            unitLabel.setText(self.t_Units)
        elif 'Energy' in prop or 'Enthalpy' in prop:
            unitLabel.setText(self.h_Units)
        elif 'Entropy' in prop:
            unitLabel.setText(self.s_Units)
        elif 'Volume' in prop:
            unitLabel.setText(self.v_Units)
        elif 'Quality' in prop:
            unitLabel.setText("")

    def calculate(self):
        """Calculate and display results for both states"""
        try:
            # Calculate State 1
            state1 = thermoState()
            prop1_1 = self.prop1Combo1.currentText()[-2:-1].lower()
            prop2_1 = self.prop2Combo1.currentText()[-2:-1].lower()
            val1_1 = float(self.prop1Value1.text())
            val2_1 = float(self.prop2Value1.text())

            if prop1_1 == prop2_1:
                self.state1Text.setText("Error: Cannot specify same property twice for State 1")
                return

            state1.setState(prop1_1, prop2_1, val1_1, val2_1, self.siRadio.isChecked())
            self.state1Text.setText(self.makeLabel(state1))

            # Calculate State 2
            state2 = thermoState()
            prop1_2 = self.prop1Combo2.currentText()[-2:-1].lower()
            prop2_2 = self.prop2Combo2.currentText()[-2:-1].lower()
            val1_2 = float(self.prop1Value2.text())
            val2_2 = float(self.prop2Value2.text())

            if prop1_2 == prop2_2:
                self.state2Text.setText("Error: Cannot specify same property twice for State 2")
                return

            state2.setState(prop1_2, prop2_2, val1_2, val2_2, self.siRadio.isChecked())
            self.state2Text.setText(self.makeLabel(state2))

            # Calculate and display differences
            delta = state2 - state1
            self.deltaText.setText(self.makeDeltaLabel(delta))

        except ValueError as e:
            self.state1Text.setText(f"Error in input values: {str(e)}")
        except Exception as e:
            self.state1Text.setText(f"Calculation error: {str(e)}")

    def makeLabel(self, state):
        """Create a formatted label for state properties"""
        return (f"Region: {state.region}\n"
                f"Pressure: {state.p:.3f} {self.p_Units}\n"
                f"Temperature: {state.t:.3f} {self.t_Units}\n"
                f"Enthalpy: {state.h:.3f} {self.h_Units}\n"
                f"Internal Energy: {state.u:.3f} {self.u_Units}\n"
                f"Entropy: {state.s:.3f} {self.s_Units}\n"
                f"Specific Volume: {state.v:.3f} {self.v_Units}\n"
                f"Quality: {state.x:.3f}")

    def makeDeltaLabel(self, delta):
        """Create a formatted label for property changes"""
        return (f"ΔPressure: {delta.p:.3f} {self.p_Units}\n"
                f"ΔTemperature: {delta.t:.3f} {self.t_Units}\n"
                f"ΔEnthalpy: {delta.h:.3f} {self.h_Units}\n"
                f"ΔInternal Energy: {delta.u:.3f} {self.u_Units}\n"
                f"ΔEntropy: {delta.s:.3f} {self.s_Units}\n"
                f"ΔSpecific Volume: {delta.v:.3f} {self.v_Units}")

class thermoState:
    def __init__(self, p=None, t=None, v=None, u=None, h=None, s=None, x=None):
        """
        This is a class I use for storing a thermodynamic state.  Calling setState requires you to specify two
        independent thermodynamic properties.  One ambiguity exists if you specify both psat and tsat.  In that
        case I assume two-phase with x=0.5
        :param p:
        :param t:
        :param v:
        :param u:
        :param h:
        :param s:
        :param x:
        """
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
        self.region = "saturated"
        self.p = p
        self.t = t
        self.v = v
        self.u = u
        self.h = h
        self.s = s
        self.x = x

    def computeProperties(self):
        """
        Assumes p and t are already calculated
        :return:
        """
        if self.region == "two-phase":
            # since two-phase, use quality to interpolate overall properties
            self.u = self.steamTable.uL_p(self.p) + self.x * (
                        self.steamTable.uV_p(self.p) - self.steamTable.uL_p(self.p))
            self.h = self.steamTable.hL_p(self.p) + self.x * (
                        self.steamTable.hV_p(self.p) - self.steamTable.hL_p(self.p))
            self.s = self.steamTable.sL_p(self.p) + self.x * (
                        self.steamTable.sV_p(self.p) - self.steamTable.sL_p(self.p))
            self.v = self.steamTable.vL_p(self.p) + self.x * (
                        self.steamTable.vV_p(self.p) - self.steamTable.vL_p(self.p))
        else:
            self.u = self.steamTable.u_pt(self.p, self.t)
            self.h = self.steamTable.h_pt(self.p, self.t)
            self.s = self.steamTable.s_pt(self.p, self.t)
            self.v = self.steamTable.v_pt(self.p, self.t)
            self.x = 1.0 if self.region == "super-heated vapor" else 0.0

    def setState(self, stProp1, stProp2, stPropVal1, stPropVal2, SI=True):
        """
        Calculates the thermodynamic state variables based on specified values.
        I have thermodynamic variables:  P, T, v, h, u, s and x (7 things) from which I am choosing two.
        Possible number of permutations:  7!/5! =42.
        But, order of the two things does not matter, so 42/2=21
        PT, Pv, Ph, Pu, Ps, Px (6)
        Tv, Th, Tu, Ts, Tx (5)
        vh, vu, vs, vx (4)
        hu, hs, hx (3)
        us, ux (2)
        sx (1)
        Total of 21 cases to deal with.  I will attack them in the order shown above
        :return: nothing
        """
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS if SI else XSteam.UNIT_SYSTEM_FLS)
        # Step 1: read which properties are being specified from the combo boxes
        SP = [stProp1, stProp2]
        SP[0] = SP[0].lower()
        SP[1] = SP[1].lower()
        f1 = float(stPropVal1)
        f2 = float(stPropVal2)
        # Step 2: select the proper case from the 21.  Note that PT is the same as TP etc.
        if SP[0] == 'p' or SP[1] == 'p':
            oFlipped = SP[0] != 'p'
            SP1 = SP[0] if oFlipped else SP[1]
            self.p = f1 if not oFlipped else f2
            tSat = self.steamTable.tsat_p(self.p)
            # case 1:  pt or tp
            if SP1 == 't':
                self.t = f2 if not oFlipped else f1
                tSat = round(tSat)  # I will compare at 3 three decimal places
                # compare T to TSat
                if self.t < tSat or self.t > tSat:
                    self.region = "sub-cooled liquid" if self.t < tSat else "super-heated vapor"
                else:  # this is ambiguous since at saturated temperature
                    self.region = "two-phase"
                    self.x = 0.5
            # case 2: pv or vp
            elif SP1 == 'v':
                self.v = f2 if not oFlipped else f1
                vf = round(self.steamTable.vL_p(self.p), 5)
                vg = round(self.steamTable.vV_p(self.p), 3)
                # compare v to vf and vg
                if self.v < vf or self.v > vg:
                    self.region = "sub-cooled liquid" if self.v < vf else "super-heated vapor"
                    # since I can't find properties using v, I will use fsolve to find T
                    dt = 1.0 if self.v > vg else -1.0
                    fn1 = lambda T: self.v - self.steamTable.v_pt(self.p, T)
                    self.t = fsolve(fn1, [tSat + dt])[0]
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.v - vf) / (vg - vf)
                    self.t = tSat
            # case 3 pu or up
            elif SP1 == 'u':
                self.u = f2 if not oFlipped else f1
                uf = round(self.steamTable.uL_p(self.p), 5)
                ug = round(self.steamTable.uV_p(self.p), 3)
                ugf = ug - uf
                # compare u to uf and ug
                if self.u < uf or self.u > ug:
                    self.region = "sub-cooled liquid" if self.u < uf else "super-heated vapor"
                    # since I can't find properties using u, I will use fsolve to find T
                    dt = 1.0 if self.u > ug else -1.0
                    fn3 = lambda T: self.u - self.steamTable.u_pt(self.p, T)
                    self.t = fsolve(fn3, [tSat + dt])[0]
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.u - uf) / (ugf)
                    self.t = tSat
            # case 4 ph or hp
            elif SP1 == 'h':
                self.h = f2 if not oFlipped else f1;
                hf = self.steamTable.hL_p(self.p)
                hg = self.steamTable.hV_p(self.p)
                hgf = hg - hf
                # compare h to hf and hg
                if self.h < hf or self.h > hg:
                    self.region = "sub-cooled liquid" if self.h < hf else "super-heated vapor"
                    self.t = self.steamTable.t_ph(self.p, self.h)
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.h - hf) / (hgf)
                    self.t = tSat
            # case 5 ps or sp
            elif SP1 == 's':
                self.s = f2 if not oFlipped else f1
                sf = self.steamTable.sL_p(self.p)
                sg = self.steamTable.sV_p(self.p)
                sgf = sg - sf
                # compare s to sf and sg
                if self.s < sf or self.s > sg:
                    self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                    self.t = self.steamTable.t_ps(self.p, self.s)
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.s - sf) / (sgf)
            # case 6 px or xp
            elif SP1 == 'x':
                self.region = "two-phase"
                self.x = f2 if not oFlipped else f1
                self.t = tSat
        elif SP[0] == 't' or SP[1] == 't':  # t and another property specified
            oFlipped = SP[0] != 't'
            SP1 = SP[0] if oFlipped else SP[1]
            self.t = f1 if not oFlipped else f2
            pSat = self.steamTable.psat_t(self.t)
            # case 7:  tv or vt
            if SP1 == 'v':
                self.v = f2 if not oFlipped else f1
                vf = self.steamTable.vL_p(pSat)
                vg = self.steamTable.vV_p(pSat)
                vgf = vg - vf
                # compare v to vf and vg
                if self.v < vf or self.v > vg:
                    self.region = "sub-cooled liquid" if self.v < vf else "super-heated vapor"
                    # since I can't find properties using v, I will use fsolve to find P
                    dp = -0.1 if self.v > vg else 0.1
                    fn3 = lambda P: [self.v - self.steamTable.v_pt(P, self.t)]
                    self.p = fsolve(fn3, [pSat + dp])[0]
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.v - vf) / (vgf)
                    self.p = pSat
            # case 8:  tu or ut
            elif SP1 == 'u':
                self.u = f2 if not oFlipped else f1
                uf = self.steamTable.uL_p(pSat)
                ug = self.steamTable.uV_p(pSat)
                ugf = ug - uf
                # compare u to uf and ug
                if self.u < uf or self.u > ug:
                    self.region = "sub-cooled liquid" if self.u < uf else "super-heated vapor"
                    # since I can't find properties using u, I will use fsolve to find P
                    dp = 0.1 if self.u > ug else -0.1
                    fn8 = lambda P: self.u - self.steamTable.u_pt(self.t, P)
                    self.p = fsolve(fn8, [pSat + dp])[0]
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.u - uf) / (ugf)
                    self.p = pSat
            # case 9:  th or ht
            elif SP1 == 'h':
                self.h = f2 if not oFlipped else f1
                hf = self.steamTable.hL_p(pSat)
                hg = self.steamTable.hV_p(pSat)
                hgf = hg - hf
                # compare h to hf and hg
                if self.h < hf or self.h > hg:
                    self.region = "sub-cooled liquid" if self.h < hf else "super-heated vapor"
                    self.p = self.steamTable.p_th(self.t, self.h)
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.p = pSat
                    self.x = (self.h - hf) / (hgf)
            # case 10:  ts or st
            elif SP1 == 's':
                self.s = f2 if not oFlipped else f1
                sf = self.steamTable.sL_p(pSat)
                sg = self.steamTable.sV_p(pSat)
                sgf = sg - sf
                # compare s to sf and sg
                if self.s < sf or self.s > sg:
                    self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                    self.p = self.steamTable.p_ts(self.t, self.s)
                    # now use P and T
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.p = pSat
                    self.x = (self.s - sf) / (sgf)
            # case 11:  tx or xt
            elif SP1 == 'x':
                self.x = f2 if not oFlipped else f1
                self.region = "two-phase"
                self.p = pSat
        elif SP[0] == 'v' or SP[1] == 'v':
            oFlipped = SP[0] != 'v'
            SP1 = SP[0] if oFlipped else SP[1]
            self.v = f1 if not oFlipped else f2
            # case 12:  vh or hv
            if SP1 == 'h':
                self.h = f2 if not oFlipped else f1

                # find p where h and v match
                def fn12(P):
                    # could be single phase or two-phase, but both v&h have to match at same x
                    hf = self.steamTable.hL_p(P)
                    hg = self.steamTable.hV_p(P)
                    hgf = hg - hf
                    vf = self.steamTable.vL_p(P)
                    vg = self.steamTable.vV_p(P)
                    vgf = vg - vf
                    if self.between(self.h, hf, hg):
                        self.x = (self.h - hf) / hgf
                        return self.v - (vf + self.x * vgf)
                    # could be single phase
                    return self.v - self.steamTable.v_ph(P, self.h)

                self.p = fsolve(fn12, [1.0])[0]
                vf = self.steamTable.vL_p(self.p)
                vg = self.steamTable.vV_p(self.p)
                tsat = self.steamTable.tsat_p(self.p)
                # compare v to vf and vg
                if self.v < vf or self.v > vg:
                    self.region = "sub-cooled liquid" if self.v < vf else "super-heated vapor"
                    dt = -1 if self.v < vf else 1
                    findtgivenv = lambda t: self.v - self.steamTable.v_pt(self.p, t)
                    self.t = fsolve(findtgivenv, [tsat + dt])[0]
                else:  # two-phase
                    self.region = "two-phase"
                    self.t = tsat
                    # first calculate quality
                    self.x = (self.v - vf) / (vg - vf)
            # case 13:  vu or uv
            elif SP1 == 'u':
                self.u = f2 if not oFlipped else f1

                # use fsolve to find P&T at this v & u
                def fn13(PT):
                    p, t = PT
                    uf = self.steamTable.uL_p(p)
                    ug = self.steamTable.uV_p(p)
                    ugf = ug - uf
                    vf = self.steamTable.vL_p(p)
                    vg = self.steamTable.vV_p(p)
                    vgf = vg - vf
                    if self.between(self.u, uf, ug):
                        self.t = self.steamTable.tsat_p(p)
                        self.x = (self.u - uf) / ugf
                        return [self.v - (vf + self.x * vgf), 0]
                    return [self.v - self.steamTable.v_pt(p, t), self.u - self.steamTable.u_pt(p, t)]

                props = fsolve(fn13, [1, 100])
                self.p = props[0]
                self.t = props[1]
                uf = self.steamTable.uL_p(self.p)
                ug = self.steamTable.uV_p(self.p)
                ugf = ug - uf
                if self.u < uf or self.u > ug:
                    self.region = "sub-cooled" if self.u < uf else "super-heated"
                else:
                    self.region = "two-phase"
                    self.x = (self.u - uf) / ugf
            # case 14:  vs os sv
            elif SP1 == 's':
                self.s = f2 if not oFlipped else f1

                def fn14(PT):
                    p, t = PT
                    sf = self.steamTable.sL_p(p)
                    sg = self.steamTable.sV_p(p)
                    sgf = sg - sf
                    vf = self.steamTable.vL_p(p)
                    vg = self.steamTable.vV_p(p)
                    vgf = vg - vf
                    if self.between(self.s, sf, sg):
                        self.x = (self.s - sf) / sgf
                        return [self.v - vf - self.x * vgf, 0.0]
                    return [self.v - self.steamTable.v_pt(p, t),
                            self.s - self.steamTable.s_pt(p, t)]

                props = fsolve(fn14, [1, self.steamTable.sV_p(1)])
                self.p = props[0]
                self.t = props[1]
                sg = self.steamTable.sV_p(self.p)
                sf = self.steamTable.sL_p(self.p)
                sgf = sg - sf
                # compare s to sf and sg
                if self.s < sf or self.s > sg:
                    self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.p = self.p
                    self.t = self.steamTable.tsat_p(self.p)
                    self.x = (self.s - sf) / (sgf)
            # case 15:  vx or xv
            elif SP1 == 'x':
                self.x = f2 if not oFlipped else f1
                self.x = self.clamp(self.x, 0.0, 1.0)
                self.region = "two-phase"

                def fn15(p):
                    vf = self.steamTable.vL_p(p)
                    vg = self.steamTable.vV_p(p)
                    vgf = vg - vf
                    return self.v - (vf + self.x * vgf)

                props = fsolve(fn15, [1])
                self.p = props[0]
                self.t = self.steamTable.tsat_p(self.p)
        elif SP[0] == 'h' or SP[1] == 'h':
            oFlipped = SP[0] != 'h'
            SP1 = SP[0] if oFlipped else SP[1]
            self.h = f1 if not oFlipped else f2
            # case 16:  hu or uh
            if SP1 == 'u':
                self.u = f2 if not oFlipped else f1

                # use fsolve to find P&T at this h & u
                def fn16(PT):
                    p, t = PT
                    uf = self.steamTable.uL_p(p)
                    ug = self.steamTable.uV_p(p)
                    ugf = ug - uf
                    hf = self.steamTable.hL_p(p)
                    hg = self.steamTable.hV_p(p)
                    hgf = hg - hf
                    if self.between(self.u, uf, ug):
                        self.x = (self.u - uf) / ugf
                        return [self.h - hf - self.x * hgf, 0.0]
                    return [self.h - self.steamTable.h_pt(p, t), self.u - self.steamTable.u_pt(p, t)]

                props = fsolve(fn16, [1, 100])
                self.p = props[0]
                self.t = props[1]
                uf = self.steamTable.uL_p(self.p)
                ug = self.steamTable.uV_p(self.p)
                ugf = ug - uf
                # compare u to uf and ug
                if self.u < uf or self.u > ug:
                    self.region = "sub-cooled liquid" if self.u < uf else "super-heated vapor"
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.u - uf) / (ugf)
            # case 17:  hs or sh
            elif SP1 == 's':
                self.s = f2 if not oFlipped else f1

                def fn17(PT):
                    p, t = PT
                    sf = self.steamTable.sL_p(p)
                    sg = self.steamTable.sV_p(p)
                    sgf = sg - sf
                    hf = self.steamTable.hL_p(p)
                    hg = self.steamTable.hV_p(p)
                    hgf = hg - hf
                    if self.between(self.s, sf, sg):
                        self.x = (self.s - sf) / sgf
                        return [self.h - hf - self.x * hgf, 0.0]
                    return [self.h - self.steamTable.h_pt(p, t), self.s - self.steamTable.s_pt(p, t)]

                props = fsolve(fn17, [1, 100])
                self.p = props[0]
                self.t = props[1]
                sf = self.steamTable.sL_p(self.p)
                sg = self.steamTable.sV_p(self.p)
                sgf = sg - sf
                # compare s to sf and sg
                if self.s < sf or self.s > sg:
                    self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.s - sf) / (sgf)
            # case 18:  hx or xh
            elif SP1 == 'x':
                self.x = f2 if not oFlipped else f1
                self.x = self.clamp(self.x, 0.0, 1.0)
                self.region = "two-phase"

                def fn18(p):
                    hf = self.steamTable.hL_p(p)
                    hg = self.steamTable.hV_p(p)
                    hgf = hg - hf
                    return self.h - (hf + self.x * hgf)

                props = fsolve(fn18, [1])
                self.p = props[0]
                self.t = self.steamTable.tsat_p(self.p)
        elif SP[0] == 'u' or SP[1] == 'u':
            oFlipped = SP[0] != 'u'
            SP1 = SP[0] if oFlipped else SP[1]
            self.u = f1 if not oFlipped else f2

            # case 19:  us or su
            if SP1 == 's':
                self.s = f2 if not oFlipped else f1

                def fn19(PT):
                    p, t = PT
                    sf = self.steamTable.sL_p(p)
                    sg = self.steamTable.sV_p(p)
                    sgf = sg - sf
                    uf = self.steamTable.uL_p(p)
                    ug = self.steamTable.uV_p(p)
                    ugf = ug - uf
                    if self.between(self.s, sf, sg):
                        self.x = (self.s - sf) / sgf
                        return [0.0, self.s - sf - self.x * sg]
                    return [self.u - self.steamTable.u_pt(p, t), self.s - self.steamTable.s_pt(p, t)]

                props = fsolve(fn19, [1, 100])
                self.p = props[0]
                self.t = props[1]
                sf = self.steamTable.sL_p(self.p)
                sg = self.steamTable.sV_p(self.p)
                sgf = sg - sf
                # compare s to sf and sg
                if self.s < sf or self.s > sg:
                    self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                else:  # two-phase
                    self.region = "two-phase"
                    # first calculate quality
                    self.x = (self.s - sf) / (sgf)
            # case 20:  ux or xu
            elif SP1 == 'x':
                self.x = f2 if not oFlipped else f1
                self.x = self.clamp(self.x, 0, 1)
                self.region = "two-phase"

                def fn20(p):
                    hf = self.steamTable.hL_p(p)
                    hg = self.steamTable.hV_p(p)
                    hgf = hg - hf
                    return self.h - (hf + self.x * hgf)

                props = fsolve(fn20, [1])
                self.p = props[0]
                self.t = self.steamTable.tsat_p(self.p)
        elif SP[0] == 's' or SP[1] == 's':
            oFlipped = SP[0] != 's'
            SP1 = SP[0] if oFlipped else SP[1]
            self.s = f1 if not oFlipped else f2
            # case 21:  sx or xs
            if SP1 == 'x':
                self.x = f2 if not oFlipped else f1
                self.x = self.clamp(self.x, 0, 1)
                self.region = "two-phase"

                def fn21(p):
                    sf = self.steamTable.sL_p(p)
                    sg = self.steamTable.sV_p(p)
                    sgf = sg - sf
                    return self.s - (sf + self.x * sgf)

                props = fsolve(fn21, [1])
                self.p = props[0]
                self.t = self.steamTable.tsat_p(self.p)
        self.computeProperties()

    def __sub__(self, other):
        delta = thermoState()
        delta.p = self.p - other.p
        delta.t = self.t - other.t
        delta.h = self.h - other.h
        delta.u = self.u - other.u
        delta.s = self.s - other.s
        delta.v = self.v - other.v
        return delta

    def clamp(self, x, low, high):
        """
        This clamps a float x between a high and low limit inclusive
        :param x:
        :param low:
        :param high:
        :return:
        """
        if x < low:
            return low
        if x > high:
            return high
        return x

    def between(self, x, low, high):
        """
        Tells if x is between low and high inclusive
        :param x:
        :param low:
        :param high:
        :return:
        """
        if x >= low and x <= high:
            return True
        return False


class ThermoCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.currentUnits = 'SI'
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
        self.connectSignals()
        self.setUnits()

    def initUI(self):
        """Initialize all UI elements"""
        self.setWindowTitle('Thermodynamic State Calculator')
        self.setGeometry(100, 100, 1000, 700)

        mainLayout = QVBoxLayout()

        # Units selection
        self.unitGroup = QGroupBox('System of Units')
        unitLayout = QHBoxLayout()
        self.siRadio = QRadioButton('SI')
        self.siRadio.setChecked(True)
        self.engRadio = QRadioButton('English')
        unitLayout.addWidget(self.siRadio)
        unitLayout.addWidget(self.engRadio)
        self.unitGroup.setLayout(unitLayout)
        mainLayout.addWidget(self.unitGroup)

        # State input section
        self.stateGroup = QGroupBox('Specified Properties')
        stateLayout = QHBoxLayout()

        # State 1 inputs
        self.state1Group = self.createStateInputGroup('State 1')
        # State 2 inputs
        self.state2Group = self.createStateInputGroup('State 2')

        stateLayout.addWidget(self.state1Group)
        stateLayout.addWidget(self.state2Group)
        self.stateGroup.setLayout(stateLayout)
        mainLayout.addWidget(self.stateGroup)

        # Calculate button
        self.calcButton = QPushButton('Calculate')
        mainLayout.addWidget(self.calcButton)

        # Results section
        self.resultsGroup = QGroupBox('State Properties')
        resultsLayout = QHBoxLayout()

        # State 1 results
        self.state1Results = QGroupBox('State 1 Properties')
        self.state1Text = QLabel('Properties will be shown here')
        state1ResLayout = QVBoxLayout()
        state1ResLayout.addWidget(self.state1Text)
        self.state1Results.setLayout(state1ResLayout)

        # State 2 results
        self.state2Results = QGroupBox('State 2 Properties')
        self.state2Text = QLabel('Properties will be shown here')
        state2ResLayout = QVBoxLayout()
        state2ResLayout.addWidget(self.state2Text)
        self.state2Results.setLayout(state2ResLayout)

        # Delta results
        self.deltaResults = QGroupBox('Property Changes (2-1)')
        self.deltaText = QLabel('Changes will be shown here')
        deltaResLayout = QVBoxLayout()
        deltaResLayout.addWidget(self.deltaText)
        self.deltaResults.setLayout(deltaResLayout)

        resultsLayout.addWidget(self.state1Results)
        resultsLayout.addWidget(self.state2Results)
        resultsLayout.addWidget(self.deltaResults)
        self.resultsGroup.setLayout(resultsLayout)
        mainLayout.addWidget(self.resultsGroup)

        self.setLayout(mainLayout)

    def createStateInputGroup(self, title):
        """Helper to create input groups for each state"""
        group = QGroupBox(title)
        layout = QVBoxLayout()

        # Property 1
        prop1Label = QLabel('Property 1:')
        prop1Combo = QComboBox()
        prop1Combo.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                             'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                             'Specific Volume (v)', 'Specific Entropy (s)'])
        prop1Value = QLineEdit('1.0')
        prop1Unit = QLabel('bar')

        # Property 2
        prop2Label = QLabel('Property 2:')
        prop2Combo = QComboBox()
        prop2Combo.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                             'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                             'Specific Volume (v)', 'Specific Entropy (s)'])
        prop2Combo.setCurrentIndex(1)  # Default to Temperature
        prop2Value = QLineEdit('100.0')
        prop2Unit = QLabel('C')

        # Add to layout
        layout.addWidget(prop1Label)
        layout.addWidget(prop1Combo)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(prop1Value)
        hbox1.addWidget(prop1Unit)
        layout.addLayout(hbox1)

        layout.addWidget(prop2Label)
        layout.addWidget(prop2Combo)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(prop2Value)
        hbox2.addWidget(prop2Unit)
        layout.addLayout(hbox2)

        group.setLayout(layout)

        # Store references as instance variables
        if title == 'State 1':
            self.prop1Combo1 = prop1Combo
            self.prop1Value1 = prop1Value
            self.prop1Unit1 = prop1Unit
            self.prop2Combo1 = prop2Combo
            self.prop2Value1 = prop2Value
            self.prop2Unit1 = prop2Unit
        else:
            self.prop1Combo2 = prop1Combo
            self.prop1Value2 = prop1Value
            self.prop1Unit2 = prop1Unit
            self.prop2Combo2 = prop2Combo
            self.prop2Value2 = prop2Value
            self.prop2Unit2 = prop2Unit

        return group

    def connectSignals(self):
        """Connect all signals to slots"""
        self.siRadio.toggled.connect(self.setUnits)
        self.engRadio.toggled.connect(self.setUnits)
        self.prop1Combo1.currentIndexChanged.connect(self.updateUnitLabels)
        self.prop2Combo1.currentIndexChanged.connect(self.updateUnitLabels)
        self.prop1Combo2.currentIndexChanged.connect(self.updateUnitLabels)
        self.prop2Combo2.currentIndexChanged.connect(self.updateUnitLabels)
        self.calcButton.clicked.connect(self.calculate)

    def setUnits(self):
        """Set the units system and convert existing values"""
        SI = self.siRadio.isChecked()
        newUnits = 'SI' if SI else 'EN'

        # Only convert if units are actually changing
        if newUnits != self.currentUnits:
            # Store current values before conversion
            state1_vals = {
                'prop1': (self.prop1Combo1.currentText(), self.prop1Value1.text()),
                'prop2': (self.prop2Combo1.currentText(), self.prop2Value1.text())
            }
            state2_vals = {
                'prop1': (self.prop1Combo2.currentText(), self.prop1Value2.text()),
                'prop2': (self.prop2Combo2.currentText(), self.prop2Value2.text())
            }

            # Update the units system
            self.currentUnits = newUnits
            self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS if SI else XSteam.UNIT_SYSTEM_FLS)

            # Define units
            if SI:
                self.p_Units = "bar"
                self.t_Units = "C"
                self.u_Units = "kJ/kg"
                self.h_Units = "kJ/kg"
                self.s_Units = "kJ/kg*C"
                self.v_Units = "m^3/kg"
            else:
                self.p_Units = "psi"
                self.t_Units = "F"
                self.u_Units = "btu/lb"
                self.h_Units = "btu/lb"
                self.s_Units = "btu/lb*F"
                self.v_Units = "ft^3/lb"

            # Convert and update State 1 values
            self.convertAndUpdateValues(state1_vals, self.prop1Value1, self.prop2Value1)

            # Convert and update State 2 values
            self.convertAndUpdateValues(state2_vals, self.prop1Value2, self.prop2Value2)

            # Update unit labels
            self.updateUnitLabels()

    def convertAndUpdateValues(self, state_vals, value_widget1, value_widget2):
        """Convert values and update the UI widgets"""
        for prop, (combo_text, value_str) in zip(['prop1', 'prop2'],
                                                 [(state_vals['prop1'][0], state_vals['prop1'][1]),
                                                  (state_vals['prop2'][0], state_vals['prop2'][1])]):
            try:
                value = float(value_str)
                prop_name = combo_text[-2:-1].lower()

                if prop == 'prop1':
                    widget = value_widget1
                else:
                    widget = value_widget2

                # Convert based on property type
                if 'Pressure' in combo_text:
                    if self.currentUnits == 'SI':
                        new_value = value * UC.bar_to_psi  # Convert from bar to psi
                    else:
                        new_value = value * UC.psi_to_bar  # Convert from psi to bar
                elif 'Temperature' in combo_text:
                    if self.currentUnits == 'SI':
                        new_value = UC.F_to_C(value)  # Convert from F to C
                    else:
                        new_value = UC.C_to_F(value)  # Convert from C to F
                elif 'Energy' in combo_text or 'Enthalpy' in combo_text:
                    if self.currentUnits == 'SI':
                        new_value = value * UC.btuperlb_to_kJperkg  # btu/lb to kJ/kg
                    else:
                        new_value = value * UC.kJperkg_to_btuperlb  # kJ/kg to btu/lb
                elif 'Entropy' in combo_text:
                    if self.currentUnits == 'SI':
                        new_value = value * UC.btuperlbF_to_kJperkgC  # btu/lb·F to kJ/kg·C
                    else:
                        new_value = value * UC.kJperkgC_to_btuperlbF  # kJ/kg·C to btu/lb·F
                elif 'Volume' in combo_text:
                    if self.currentUnits == 'SI':
                        new_value = value * UC.ft3perlb_to_m3perkg  # ft³/lb to m³/kg
                    else:
                        new_value = value * UC.m3perkg_to_ft3perlb  # m³/kg to ft³/lb
                elif 'Quality' in combo_text:
                    new_value = value  # Quality is unitless

                widget.setText(f"{new_value:.3f}")

            except ValueError:
                # Handle invalid input (leave as is)
                pass

    def updateUnitLabels(self):
        """Update all unit labels"""
        self.updatePropertyUnits(self.prop1Combo1, self.prop1Unit1)
        self.updatePropertyUnits(self.prop2Combo1, self.prop2Unit1)
        self.updatePropertyUnits(self.prop1Combo2, self.prop1Unit2)
        self.updatePropertyUnits(self.prop2Combo2, self.prop2Unit2)

    def updatePropertyUnits(self, combo, unitLabel):
        """Update unit label for a single property"""
        prop = combo.currentText()
        if 'Pressure' in prop:
            unitLabel.setText(self.p_Units)
        elif 'Temperature' in prop:
            unitLabel.setText(self.t_Units)
        elif 'Energy' in prop or 'Enthalpy' in prop:
            unitLabel.setText(self.h_Units)
        elif 'Entropy' in prop:
            unitLabel.setText(self.s_Units)
        elif 'Volume' in prop:
            unitLabel.setText(self.v_Units)
        elif 'Quality' in prop:
            unitLabel.setText("")

    def calculate(self):
        """Perform calculations for both states"""
        try:
            # Calculate State 1
            state1 = thermoState()
            prop1_1 = self.prop1Combo1.currentText()[-2:-1].lower()
            prop2_1 = self.prop2Combo1.currentText()[-2:-1].lower()
            val1_1 = float(self.prop1Value1.text())
            val2_1 = float(self.prop2Value1.text())

            if prop1_1 == prop2_1:
                self.state1Text.setText("Error: Cannot specify same property twice for State 1")
                return

            state1.setState(prop1_1, prop2_1, val1_1, val2_1, self.siRadio.isChecked())
            self.state1Text.setText(self.makeLabel(state1))

            # Calculate State 2
            state2 = thermoState()
            prop1_2 = self.prop1Combo2.currentText()[-2:-1].lower()
            prop2_2 = self.prop2Combo2.currentText()[-2:-1].lower()
            val1_2 = float(self.prop1Value2.text())
            val2_2 = float(self.prop2Value2.text())

            if prop1_2 == prop2_2:
                self.state2Text.setText("Error: Cannot specify same property twice for State 2")
                return

            state2.setState(prop1_2, prop2_2, val1_2, val2_2, self.siRadio.isChecked())
            self.state2Text.setText(self.makeLabel(state2))

            # Calculate and display differences
            delta = state2 - state1
            self.deltaText.setText(self.makeDeltaLabel(delta))

        except ValueError as e:
            self.state1Text.setText(f"Error in input values: {str(e)}")
        except Exception as e:
            self.state1Text.setText(f"Calculation error: {str(e)}")

    def makeLabel(self, state):
        """Create formatted text for state properties"""
        return (f"Region: {state.region}\n"
                f"Pressure: {state.p:.3f} {self.p_Units}\n"
                f"Temperature: {state.t:.3f} {self.t_Units}\n"
                f"Enthalpy: {state.h:.3f} {self.h_Units}\n"
                f"Internal Energy: {state.u:.3f} {self.u_Units}\n"
                f"Entropy: {state.s:.3f} {self.s_Units}\n"
                f"Specific Volume: {state.v:.3f} {self.v_Units}\n"
                f"Quality: {state.x:.3f}")

    def makeDeltaLabel(self, delta):
        """Create formatted text for property changes"""
        return (f"ΔPressure: {delta.p:.3f} {self.p_Units}\n"
                f"ΔTemperature: {delta.t:.3f} {self.t_Units}\n"
                f"ΔEnthalpy: {delta.h:.3f} {self.h_Units}\n"
                f"ΔInternal Energy: {delta.u:.3f} {self.u_Units}\n"
                f"ΔEntropy: {delta.s:.3f} {self.s_Units}\n"
                f"ΔSpecific Volume: {delta.v:.3f} {self.v_Units}")


def main():
    app = QApplication(sys.argv)
    calculator = ThermoCalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()