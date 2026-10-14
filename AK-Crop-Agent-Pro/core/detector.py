import cv2
import numpy as np


def detect_cards(image, min_area=10000):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(
        gray,
        245,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    cv2.imwrite("debug_threshold.png", thresh)

    h, w = thresh.shape

    row_sum = np.sum(thresh > 0, axis=1)

    active_rows = row_sum > (w * 0.20)

    regions = []

    start = None

    for y in range(h):

        if active_rows[y] and start is None:
            start = y

        elif not active_rows[y] and start is not None:

            if (y - start) > 150:
                regions.append((start, y))

            start = None

    if start is not None:
        regions.append((start, h))

    cards = []

    for start, end in regions:

        region = thresh[start:end, :]

        cols = np.sum(region > 0, axis=0)

        xs = np.where(cols > 80)[0]

        if len(xs) == 0:
            continue

        # Linken Rand vorsichtig beschneiden
        x1 = max(0, int(xs.min()) + 5)

        # Rechten Rand vorsichtig beschneiden
        x2 = min(w, int(xs.max()) + 5)

        # Oberen Rand
        y1 = max(0, start - 10)

        # ==================================================
        # UNTERER SICHERHEITSRAND
        #
        # HIER DEN WERT ÄNDERN
        #
        # 100  = großzügig
        # 150  = sehr großzügig
        # 200  = extrem großzügig
        #
        # Beispiel:
        # y2 = min(h, end + 200)
        # ==================================================

        y2 = min(h, end + 80)

        card = image[y1:y2, x1:x2]

        cards.append((y1, card))

    cards.sort(key=lambda t: t[0])

    return [c[1] for c in cards]