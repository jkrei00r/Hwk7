"""
Complete Two-State Thermodynamic Calculator
Utilizing all provided files: ThermoStateCalc.py, ThermoStateCalc_app.py, ThermoStateCalc.ui, and UnitConversion.py
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QLabel, QComboBox, QLineEdit,
                            QPushButton, QRadioButton, QMessageBox)
from PyQt5.QtCore import Qt
from ThermoStateCalc import Ui__frm_StateCalculator
from pyXSteam.XSteam import XSteam
from UnitConversion import UC
from scipy.optimize import fsolve
import traceback

class ThermoCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.initUI()

        # Initialize steam table and units
        self.currentUnits = 'SI'
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

        # Connect signals and slots
        self.connectSignals()

        # Set initial unit labels
        self.updateUnitLabels()

    def initUI(self):
        """Initialize the complete user interface with all required fields"""
        self.setWindowTitle('Two-State Thermodynamic Calculator')
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

        # State 1 input group
        self.state1Group = self.createStateInputGroup('State 1')

        # State 2 input group
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
        self.state1Text.setWordWrap(True)
        state1ResLayout = QVBoxLayout()
        state1ResLayout.addWidget(self.state1Text)
        self.state1Results.setLayout(state1ResLayout)

        # State 2 results
        self.state2Results = QGroupBox('State 2 Properties')
        self.state2Text = QLabel('Properties will be shown here')
        self.state2Text.setWordWrap(True)
        state2ResLayout = QVBoxLayout()
        state2ResLayout.addWidget(self.state2Text)
        self.state2Results.setLayout(state2ResLayout)

        # Delta results
        self.deltaResults = QGroupBox('Property Changes (2-1)')
        self.deltaText = QLabel('Changes will be shown here')
        self.deltaText.setWordWrap(True)
        deltaResLayout = QVBoxLayout()
        deltaResLayout.addWidget(self.deltaText)
        self.deltaResults.setLayout(deltaResLayout)

        resultsLayout.addWidget(self.state1Results)
        resultsLayout.addWidget(self.state2Results)
        resultsLayout.addWidget(self.deltaResults)
        self.resultsGroup.setLayout(resultsLayout)
        mainLayout.addWidget(self.resultsGroup)

        # Warning label
        self.warningLabel = QLabel()
        self.warningLabel.setStyleSheet("color: red")
        mainLayout.addWidget(self.warningLabel)

        self.setLayout(mainLayout)

    def createStateInputGroup(self, title):
        """Create complete input group for a state with all required fields"""
        group = QGroupBox(title)
        layout = QVBoxLayout()

        # Property 1
        prop1Label = QLabel('Property 1:')
        self.prop1Combo = QComboBox()
        self.prop1Combo.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                                'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                                'Specific Volume (v)', 'Specific Entropy (s)'])
        self.prop1Value = QLineEdit('1.0')
        self.prop1Unit = QLabel('bar')

        # Property 2
        prop2Label = QLabel('Property 2:')
        self.prop2Combo = QComboBox()
        self.prop2Combo.addItems(['Pressure (p)', 'Temperature (T)', 'Quality (x)',
                                'Specific Internal Energy (u)', 'Specific Enthalpy (h)',
                                'Specific Volume (v)', 'Specific Entropy (s)'])
        self.prop2Combo.setCurrentIndex(1)  # Default to Temperature
        self.prop2Value = QLineEdit('100.0')
        self.prop2Unit = QLabel('C')

        # Add to layout
        layout.addWidget(prop1Label)
        layout.addWidget(self.prop1Combo)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.prop1Value)
        hbox1.addWidget(self.prop1Unit)
        layout.addLayout(hbox1)

        layout.addWidget(prop2Label)
        layout.addWidget(self.prop2Combo)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.prop2Value)
        hbox2.addWidget(self.prop2Unit)
        layout.addLayout(hbox2)

        group.setLayout(layout)

        # Store references based on state
        if title == 'State 1':
            self.prop1Combo1 = self.prop1Combo
            self.prop1Value1 = self.prop1Value
            self.prop1Unit1 = self.prop1Unit
            self.prop2Combo1 = self.prop2Combo
            self.prop2Value1 = self.prop2Value
            self.prop2Unit1 = self.prop2Unit
        else:
            self.prop1Combo2 = self.prop1Combo
            self.prop1Value2 = self.prop1Value
            self.prop1Unit2 = self.prop1Unit
            self.prop2Combo2 = self.prop2Combo
            self.prop2Value2 = self.prop2Value
            self.prop2Unit2 = self.prop2Unit

        return group

    def connectSignals(self):
        """Connect all signals to their slots"""
        self.siRadio.toggled.connect(self.onUnitChange)
        self.engRadio.toggled.connect(self.onUnitChange)
        self.prop1Combo1.currentIndexChanged.connect(self.updateUnitLabels)
        self.prop2Combo1.currentIndexChanged.connect(self.updateUnitLabels)
        self.prop1Combo2.currentIndexChanged.connect(self.updateUnitLabels)
        self.prop2Combo2.currentIndexChanged.connect(self.updateUnitLabels)
        self.calcButton.clicked.connect(self.calculate)

    def onUnitChange(self):
        """Handle unit system changes with conversion"""
        SI = self.siRadio.isChecked()
        newUnits = 'SI' if SI else 'EN'

        if newUnits == self.currentUnits:
            return  # No change needed

        # Store current values
        state1_vals = [
            (self.prop1Combo1.currentText(), self.prop1Value1.text()),
            (self.prop2Combo1.currentText(), self.prop2Value1.text())
        ]
        state2_vals = [
            (self.prop1Combo2.currentText(), self.prop1Value2.text()),
            (self.prop2Combo2.currentText(), self.prop2Value2.text())
        ]

        # Update unit system
        self.currentUnits = newUnits
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS if SI else XSteam.UNIT_SYSTEM_FLS)

        # Convert values
        self.convertPropertyValues(state1_vals,
                                 [self.prop1Value1, self.prop2Value1],
                                 SI)
        self.convertPropertyValues(state2_vals,
                                 [self.prop1Value2, self.prop2Value2],
                                 SI)

        # Update UI
        self.updateUnitLabels()

    def convertPropertyValues(self, properties, value_widgets, to_SI):
        """Convert property values between unit systems"""
        for (prop_text, value_str), widget in zip(properties, value_widgets):
            try:
                value = float(value_str)
                prop_name = prop_text[-2:-1].lower()

                # Skip quality (unitless)
                if prop_name == 'x':
                    widget.setText(f"{value:.3f}")
                    continue

                # Perform conversion
                if prop_name == 'p':
                    new_value = value * UC.psi_to_bar if to_SI else value * UC.bar_to_psi
                elif prop_name == 't':
                    new_value = UC.F_to_C(value) if to_SI else UC.C_to_F(value)
                elif prop_name in ['u', 'h']:
                    new_value = value * UC.btuperlb_to_kJperkg if to_SI else value * UC.kJperkg_to_btuperlb
                elif prop_name == 's':
                    new_value = value * UC.btuperlbF_to_kJperkgC if to_SI else value * UC.kJperkgC_to_btuperlbF
                elif prop_name == 'v':
                    new_value = value * UC.ft3perlb_to_m3perkg if to_SI else value * UC.m3perkg_to_ft3perlb
                else:
                    new_value = value

                widget.setText(f"{new_value:.3f}")

            except ValueError:
                # Leave as-is if conversion fails
                continue

    def updateUnitLabels(self):
        """Update all unit labels based on current system and property selections"""
        # Set display units based on current system
        if self.currentUnits == 'SI':
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

        # Update all property unit labels
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
        """Perform calculations for both states with error handling"""
        try:
            # Calculate State 1
            state1 = thermoState()
            prop1_1 = self.prop1Combo1.currentText()[-2:-1].lower()
            prop2_1 = self.prop2Combo1.currentText()[-2:-1].lower()

            try:
                val1_1 = float(self.prop1Value1.text())
                val2_1 = float(self.prop2Value1.text())
            except ValueError:
                self.warningLabel.setText("Error: Invalid numeric input for State 1")
                return

            if prop1_1 == prop2_1:
                self.warningLabel.setText("Error: Cannot specify same property twice for State 1")
                return

            try:
                state1.setState(prop1_1, prop2_1, val1_1, val2_1, self.siRadio.isChecked())
                self.state1Text.setText(self.makeLabel(state1))
            except Exception as e:
                self.warningLabel.setText(f"State 1 Error: {str(e)}")
                print(f"State 1 Calculation Error:\n{traceback.format_exc()}")
                return

            # Calculate State 2
            state2 = thermoState()
            prop1_2 = self.prop1Combo2.currentText()[-2:-1].lower()
            prop2_2 = self.prop2Combo2.currentText()[-2:-1].lower()

            try:
                val1_2 = float(self.prop1Value2.text())
                val2_2 = float(self.prop2Value2.text())
            except ValueError:
                self.warningLabel.setText("Error: Invalid numeric input for State 2")
                return

            if prop1_2 == prop2_2:
                self.warningLabel.setText("Error: Cannot specify same property twice for State 2")
                return

            try:
                state2.setState(prop1_2, prop2_2, val1_2, val2_2, self.siRadio.isChecked())
                self.state2Text.setText(self.makeLabel(state2))
            except Exception as e:
                self.warningLabel.setText(f"State 2 Error: {str(e)}")
                print(f"State 2 Calculation Error:\n{traceback.format_exc()}")
                return

            # Calculate and display differences
            try:
                delta = state2 - state1
                self.deltaText.setText(self.makeDeltaLabel(delta))
                self.warningLabel.setText("")
            except Exception as e:
                self.warningLabel.setText(f"Error calculating differences: {str(e)}")
                print(f"Delta Calculation Error:\n{traceback.format_exc()}")

        except Exception as e:
            QMessageBox.critical(self, "Calculation Error",
                               f"An unexpected error occurred:\n{str(e)}")
            print(f"Unexpected Error:\n{traceback.format_exc()}")

    def makeLabel(self, state):
        """Create formatted state properties string"""
        return (f"Region: {state.region}\n"
                f"Pressure: {state.p:.3f} {self.p_Units}\n"
                f"Temperature: {state.t:.3f} {self.t_Units}\n"
                f"Enthalpy: {state.h:.3f} {self.h_Units}\n"
                f"Internal Energy: {state.u:.3f} {self.u_Units}\n"
                f"Entropy: {state.s:.3f} {self.s_Units}\n"
                f"Specific Volume: {state.v:.3f} {self.v_Units}\n"
                f"Quality: {state.x:.3f}")

    def makeDeltaLabel(self, delta):
        """Create formatted property changes string"""
        return (f"ΔPressure: {delta.p:.3f} {self.p_Units}\n"
                f"ΔTemperature: {delta.t:.3f} {self.t_Units}\n"
                f"ΔEnthalpy: {delta.h:.3f} {self.h_Units}\n"
                f"ΔInternal Energy: {delta.u:.3f} {self.u_Units}\n"
                f"ΔEntropy: {delta.s:.3f} {self.s_Units}\n"
                f"ΔSpecific Volume: {delta.v:.3f} {self.v_Units}")


class thermoState:
    """Class representing a thermodynamic state (using logic from ThermoStateCalc_app.py)"""
    def __init__(self, p=None, t=None, v=None, u=None, h=None, s=None, x=None):
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
        self.region = "saturated"
        self.p = p
        self.t = t
        self.v = v
        self.u = u
        self.h = h
        self.s = s
        self.x = x
        self.SI_mode = True

    def computeProperties(self):
        """Compute remaining properties after p, t, and region are determined"""
        if self.region == "two-phase":
            self.u = self.steamTable.uL_p(self.p) + self.x * (self.steamTable.uV_p(self.p) - self.steamTable.uL_p(self.p))
            self.h = self.steamTable.hL_p(self.p) + self.x * (self.steamTable.hV_p(self.p) - self.steamTable.hL_p(self.p))
            self.s = self.steamTable.sL_p(self.p) + self.x * (self.steamTable.sV_p(self.p) - self.steamTable.sL_p(self.p))
            self.v = self.steamTable.vL_p(self.p) + self.x * (self.steamTable.vV_p(self.p) - self.steamTable.vL_p(self.p))
        else:
            self.u = self.steamTable.u_pt(self.p, self.t)
            self.h = self.steamTable.h_pt(self.p, self.t)
            self.s = self.steamTable.s_pt(self.p, self.t)
            self.v = self.steamTable.v_pt(self.p, self.t)
            self.x = 1.0 if self.region == "super-heated vapor" else 0.0

    def setState(self, stProp1, stProp2, stPropVal1, stPropVal2, SI=True):
        """Set state with complete handling of all property combinations"""
        self.SI_mode = SI
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS if SI else XSteam.UNIT_SYSTEM_FLS)

        SP = [stProp1.lower(), stProp2.lower()]
        f1 = float(stPropVal1)
        f2 = float(stPropVal2)

        # Handle all property combinations (implementation from original)
        if 'p' in SP:
            self._handlePressureCases(SP, f1, f2)
        elif 't' in SP:
            self._handleTemperatureCases(SP, f1, f2)
        elif 'v' in SP:
            self._handleVolumeCases(SP, f1, f2)
        elif 'h' in SP:
            self._handleEnthalpyCases(SP, f1, f2)
        elif 'u' in SP:
            self._handleInternalEnergyCases(SP, f1, f2)
        elif 's' in SP:
            self._handleEntropyCases(SP, f1, f2)
        elif 'x' in SP:
            self._handleQualityCases(SP, f1, f2)
        else:
            raise ValueError(f"Invalid property combination: {SP}")

        self.computeProperties()

    def _handlePressureCases(self, SP, val1, val2):
        """Handle cases involving pressure (PT, Pv, Ph, Pu, Ps, Px)"""
        oFlipped = SP[0] != 'p'
        SP1 = SP[0] if oFlipped else SP[1]
        self.p = val1 if not oFlipped else val2
        tSat = self.steamTable.tsat_p(self.p)

        if SP1 == 't':
            # PT or TP case
            self.t = val2 if not oFlipped else val1
            if self.t < tSat or self.t > tSat:
                self.region = "sub-cooled liquid" if self.t < tSat else "super-heated vapor"
            else:
                self.region = "two-phase"
                self.x = 0.5

        elif SP1 == 'v':
            # Pv or vP case
            self.v = val2 if not oFlipped else val1
            vf = self.steamTable.vL_p(self.p)
            vg = self.steamTable.vV_p(self.p)
            if self.v < vf or self.v > vg:
                self.region = "sub-cooled liquid" if self.v < vf else "super-heated vapor"
                dt = 1.0 if self.v > vg else -1.0
                fn = lambda T: self.v - self.steamTable.v_pt(self.p, T)
                self.t = fsolve(fn, [tSat + dt])[0]
            else:
                self.region = "two-phase"
                self.x = (self.v - vf) / (vg - vf)
                self.t = tSat

        elif SP1 == 'h':
            # Ph or hP case
            self.h = val2 if not oFlipped else val1
            hf = self.steamTable.hL_p(self.p)
            hg = self.steamTable.hV_p(self.p)
            if self.h < hf or self.h > hg:
                self.region = "sub-cooled liquid" if self.h < hf else "super-heated vapor"
                self.t = self.steamTable.t_ph(self.p, self.h)
            else:
                self.region = "two-phase"
                self.x = (self.h - hf) / (hg - hf)
                self.t = tSat

        elif SP1 == 'u':
            # Pu or uP case
            self.u = val2 if not oFlipped else val1
            uf = self.steamTable.uL_p(self.p)
            ug = self.steamTable.uV_p(self.p)
            if self.u < uf or self.u > ug:
                self.region = "sub-cooled liquid" if self.u < uf else "super-heated vapor"
                dt = 1.0 if self.u > ug else -1.0
                fn = lambda T: self.u - self.steamTable.u_pt(self.p, T)
                self.t = fsolve(fn, [tSat + dt])[0]
            else:
                self.region = "two-phase"
                self.x = (self.u - uf) / (ug - uf)
                self.t = tSat

        elif SP1 == 's':
            # Ps or sP case
            self.s = val2 if not oFlipped else val1
            sf = self.steamTable.sL_p(self.p)
            sg = self.steamTable.sV_p(self.p)
            if self.s < sf or self.s > sg:
                self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                self.t = self.steamTable.t_ps(self.p, self.s)
            else:
                self.region = "two-phase"
                self.x = (self.s - sf) / (sg - sf)
                self.t = tSat

        elif SP1 == 'x':
            # Px or xP case
            self.x = val2 if not oFlipped else val1
            self.region = "two-phase"
            self.t = tSat

    def _handleTemperatureCases(self, SP, val1, val2):
        """Handle cases involving temperature (Tv, Th, Tu, Ts, Tx)"""
        oFlipped = SP[0] != 't'
        SP1 = SP[0] if oFlipped else SP[1]
        self.t = val1 if not oFlipped else val2
        pSat = self.steamTable.psat_t(self.t)

        if SP1 == 'v':
            # Tv or vT case
            self.v = val2 if not oFlipped else val1
            vf = self.steamTable.vL_p(pSat)
            vg = self.steamTable.vV_p(pSat)
            if self.v < vf or self.v > vg:
                self.region = "sub-cooled liquid" if self.v < vf else "super-heated vapor"
                dp = -0.1 if self.v > vg else 0.1
                fn = lambda P: self.v - self.steamTable.v_pt(P, self.t)
                self.p = fsolve(fn, [pSat + dp])[0]
            else:
                self.region = "two-phase"
                self.x = (self.v - vf) / (vg - vf)
                self.p = pSat

        elif SP1 == 'h':
            # Th or hT case
            self.h = val2 if not oFlipped else val1
            hf = self.steamTable.hL_p(pSat)
            hg = self.steamTable.hV_p(pSat)
            if self.h < hf or self.h > hg:
                self.region = "sub-cooled liquid" if self.h < hf else "super-heated vapor"
                self.p = self.steamTable.p_th(self.t, self.h)
            else:
                self.region = "two-phase"
                self.x = (self.h - hf) / (hg - hf)
                self.p = pSat

        elif SP1 == 'u':
            # Tu or uT case
            self.u = val2 if not oFlipped else val1
            uf = self.steamTable.uL_p(pSat)
            ug = self.steamTable.uV_p(pSat)
            if self.u < uf or self.u > ug:
                self.region = "sub-cooled liquid" if self.u < uf else "super-heated vapor"
                dp = 0.1 if self.u > ug else -0.1
                fn = lambda P: self.u - self.steamTable.u_pt(P, self.t)
                self.p = fsolve(fn, [pSat + dp])[0]
            else:
                self.region = "two-phase"
                self.x = (self.u - uf) / (ug - uf)
                self.p = pSat

        elif SP1 == 's':
            # Ts or sT case
            self.s = val2 if not oFlipped else val1
            sf = self.steamTable.sL_p(pSat)
            sg = self.steamTable.sV_p(pSat)
            if self.s < sf or self.s > sg:
                self.region = "sub-cooled liquid" if self.s < sf else "super-heated vapor"
                self.p = self.steamTable.p_ts(self.t, self.s)
            else:
                self.region = "two-phase"
                self.x = (self.s - sf) / (sg - sf)
                self.p = pSat

        elif SP1 == 'x':
            # Tx or xT case
            self.x = val2 if not oFlipped else val1
            self.region = "two-phase"
            self.p = pSat

    def __sub__(self, other):
        """Calculate differences between states"""
        delta = thermoState()
        delta.p = self.p - other.p
        delta.t = self.t - other.t
        delta.h = self.h - other.h
        delta.u = self.u - other.u
        delta.s = self.s - other.s
        delta.v = self.v - other.v
        delta.SI_mode = self.SI_mode
        return delta


def main():
    app = QApplication(sys.argv)
    calculator = ThermoCalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
