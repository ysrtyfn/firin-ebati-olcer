import math

from Sabitler import Sabitler
from Nokta import Nokta


class Araclar:
    nokta_capi = Sabitler.nokta_capi
    nokta_rengi = Sabitler.nokta_rengi
    daire_rengi = Sabitler.daire_rengi
    cizgi_rengi = Sabitler.cizgi_rengi
    cizgi_kalinligi = Sabitler.cizgi_kalinligi

    def px_to_mm(self, pixel_value):
        ref_mesafe_mm = Sabitler.ref_mesafe_mm
        ref_mesafe_px = Sabitler.ref_mesafe_px

        return ref_mesafe_mm * pixel_value / ref_mesafe_px

    def define_circle(self, cv2, image, olc_daire_nokt):
        """
        Returns the center and radius of the circle passing the given 3 points.
        In case the 3 points form a line, returns (None, infinity).
        """

        if len(olc_daire_nokt) != 3:
            return (None, np.inf)

        nokta1 = olc_daire_nokt[0]
        nokta2 = olc_daire_nokt[1]
        nokta3 = olc_daire_nokt[2]

        temp = nokta2.X * nokta2.X + nokta2.Y * nokta2.Y
        bc = (nokta1.X * nokta1.X + nokta1.Y * nokta1.Y - temp) / 2
        cd = (temp - nokta3.X * nokta3.X - nokta3.Y * nokta3.Y) / 2
        det = (nokta1.X - nokta2.X) * (nokta2.Y - nokta3.Y) - (nokta2.X - nokta3.X) * (nokta1.Y - nokta2.Y)

        if abs(det) < 1.0e-6:
            return (None, np.inf)

        # Center of circle
        cx = (bc * (nokta2.Y - nokta3.Y) - cd * (nokta1.Y - nokta2.Y)) / det
        cy = ((nokta1.X - nokta2.X) * cd - (nokta2.X - nokta3.X) * bc) / det

        radius = math.sqrt((cx - nokta1.X) ** 2 + (cy - nokta1.Y) ** 2)

        cx = int(cx)
        cy = int(cy)
        radius = int(radius)

        daire = Daire(cx, cy, radius)
        cv2.circle(image, (cx, cy), radius, self.daire_rengi, -1)
        return daire

    def nokta_cizgi_arasi_mesafeyi_hesapla(self, cv2, image, noktalar):

        # Ölçüm Noktası
        x0 = noktalar[0].X
        y0 = noktalar[0].Y

        # Çizgi Noktaları
        x1 = noktalar[1].X
        y1 = noktalar[1].Y
        x2 = noktalar[2].X
        y2 = noktalar[2].Y

        m = 0
        k = y0
        xs1 = 0
        ys1 = 0
        xs2 = 0
        ys2 = 0

        if (x2 - x1) == 0:
            # Kesişim Noktası
            xk = x2
            yk = y0

            xs1 = x1
            ys1 = -10000
            xs2 = x2
            ys2 = 10000

        else:
            m = (y2 - y1) / (x2 - x1)
            k = y2 - m * x2

            # Kesişim Noktası
            xk = int((x0 + m * y0 - m * k) / (m * m + 1))
            yk = int(m * xk + k)

            xs1 = -10000
            ys1 = int(m * xs1 + k)
            xs2 = 10000
            ys2 = int(m * xs2 + k)

        cv2.line(image, (x0, y0), (xk, yk), self.cizgi_rengi, self.cizgi_kalinligi)
        cv2.line(image, (xs1, ys1), (xs2, ys2), self.cizgi_rengi, self.cizgi_kalinligi)

        nokta_1 = Nokta(x0, y0)
        nokta_2 = Nokta(xk, yk)

        hesap_sonuclari = nokta_1.distance(nokta_2)
        # mesafe = (abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / ((y2-y1)**2 + (x2-x1)**2)**(1/2.0))
        return hesap_sonuclari
