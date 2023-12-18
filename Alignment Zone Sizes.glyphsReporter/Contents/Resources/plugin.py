# encoding: utf-8
from __future__ import division, print_function, unicode_literals
from GlyphsApp.plugins import *

class AlignmentZoneSizes(ReporterPlugin):
	
	
	@objc.python_method
	def settings(self):

		# The name as it will appear in the View menu
		self.menuName = 'Alignment Zones Sizes'

	@objc.python_method
	def conditionsAreMetForDrawing(self):
		"""
		Don't activate if text or pan (hand) tool are active.
		"""
		currentController = self.controller.view().window().windowController()
		if currentController:
			tool = currentController.toolDrawDelegate()
			textToolIsActive = tool.isKindOfClass_(NSClassFromString("GlyphsToolText"))
			handToolIsActive = tool.isKindOfClass_(NSClassFromString("GlyphsToolHand"))
			if not textToolIsActive and not handToolIsActive: 
				return True
		return False

	@objc.python_method
	def foreground(self, layer):

		if not self.conditionsAreMetForDrawing():
			return

		Font = Glyphs.font
		# Set the variable of current master
		thisMaster = Font.selectedFontMaster

		# For each alignment zone in the current master
		for zone in thisMaster.alignmentZones:

			color_for_light_appearance = Glyphs.colorDefaults['GSColorZones']
			color_for_dark_appearance = Glyphs.colorDefaults['GSColorZonesDark']
			fontcolor = color_for_light_appearance.colorWithAlphaComponent_(1)
			# Get alignment zone position + its size
			self.drawTextAtPoint(str(zone.size), NSPoint(-10, zone.position), 10, fontcolor, align="right")
		
