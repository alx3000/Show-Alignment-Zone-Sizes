# encoding: utf-8

from GlyphsApp.plugins import *
import math

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
	def foregroundInViewCoords(self):

		if not self.conditionsAreMetForDrawing():
			return

		layer = self.controller.graphicView().activeLayer()
		thisMaster = layer.master

		if self.black:
			color = Glyphs.colorDefaults['GSColorZonesDark']
		else:
			color = Glyphs.colorDefaults['GSColorZones']
		fontcolor = color.colorWithAlphaComponent_(1)
		activePosition = self.controller.graphicView().activePosition()
		italicAngle = layer.italicAngle
		transform = None
		scale = self._scale
		if abs(italicAngle) > 0.001:
			transform = NSAffineTransform.new()
			slant = math.tan(math.radians(italicAngle))
			transform.shearXBy_atCenter_(slant, layer.slantHeight())

		# For each alignment zone in the current master
		for zone in thisMaster.alignmentZones:
			# Get alignment zone position + its size
			pos = NSMakePoint(-4, zone.position)
			
			if transform:
				pos = transform.transformPoint_(pos)

			pos.x = pos.x * scale + activePosition.x
			pos.y = pos.y * scale + activePosition.y
			if zone.size > 0:
				pos.y += 4
			else:
				pos.y -= 3
			string = NSString.stringWithString_(str(int(zone.size)))
			string.drawAtPoint_color_alignment_handleSize_(pos, fontcolor, 5, -1)
