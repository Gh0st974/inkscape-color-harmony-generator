import inkex
from inkex import Rectangle
import colorsys

class ColorHarmonyGenerator(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--base_color", type=str, default="#ff0000")
        pars.add_argument("--rule", default="analogous")

    def effect(self):
        # 1. Récupération de la couleur choisie
        color_str = self.options.base_color.replace("0x", "#").split(';')[0]
        try:
            r, g, b = inkex.Color(color_str).to_rgb()
            r, g, b = r/255.0, g/255.0, b/255.0
        except:
            r, g, b = 1.0, 0.0, 0.0 

        h, l, s = colorsys.rgb_to_hls(r, g, b)
        palette = []

        # 2. Logique des harmonies (inchangée)
        for i in range(5):
            new_h, new_l, new_s = h, l, s
            if self.options.rule == "analogous":
                new_h = (h + ((i - 2) * 0.05)) % 1.0
            elif self.options.rule == "monochrome":
                new_l = max(0, min(1, l + ((i - 2) * 0.15)))
            elif self.options.rule == "complementary":
                if i >= 3: new_h = (h + 0.5) % 1.0
                new_l = max(0, min(1, l + ((i - 2) * 0.1)))
            elif self.options.rule == "triad":
                if i == 1: new_h = (h + 0.33) % 1.0
                if i == 2: new_h = (h + 0.66) % 1.0
                if i >= 3: new_l = max(0, min(1, l - 0.2))
            elif self.options.rule == "shades":
                new_l = max(0.05, min(0.95, 0.9 - (i * 0.2)))

            rgb = colorsys.hls_to_rgb(new_h, new_l, new_s)
            palette.append('#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))

        # 3. POSITIONNEMENT HORS-PAGE (AU-DESSUS)
        layer = self.svg.get_current_layer()
        size = self.svg.unittouu('50px')
        spacing = self.svg.unittouu('10px')
        
        # Calcul du Y négatif : on monte de la taille du carré + une marge
        # Cela place le bas des carrés 10px au dessus du bord de la feuille
        y_pos = -(size + self.svg.unittouu('20px')) 
        
        for i, hex_col in enumerate(palette):
            rect = Rectangle()
            # X reste à 10px du bord gauche
            x_pos = self.svg.unittouu('10px') + (i * (size + spacing))
            
            rect.set('x', str(x_pos))
            rect.set('y', str(y_pos)) # Valeur négative = au-dessus de la feuille
            rect.set('width', str(size))
            rect.set('height', str(size))
            rect.style = {'fill': hex_col, 'stroke': 'none'}
            layer.append(rect)

if __name__ == '__main__':
    ColorHarmonyGenerator().run()
