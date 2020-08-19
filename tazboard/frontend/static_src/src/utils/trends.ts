/**
 *  Diese Funktion versucht zwei werte ohne weitere information in trendkategorien einzuordnen.
 *  Profan: bei zwei gegeben werten eine Aussage darueber treffen, wie stark der zweite Wert groesser
 *  oder kleiner als der erste ist. Dabei gibt es menschliche vorgaben wie
 *  "wenn es fast gleich ist, soll es als unveraendert angezeigt werden." und
 *  "Es ist das Gleiche, ob der zweite Wert 10mal groesser ist oder 100mal groesser ist"

 *  @param tx1: erster Wert als int oder float
 *  @param tx2: zweiter Wert als int oder float
 *  @param interval: wieviele intervalle gibt es als int - die anzahl verdoppelt sich, da die Richtung
 *                  (hoch oder runter) seperat als vorzeichen angegeben wird. Wird ein Interval von 5
 *                  angegeben, sind die rueckgabewerte 0,1,2,3,4 plus die Richtung
 *                  (gedanklich default fuer 5: gleich,leicht hoch,etwas mehr hoch, hoch, krass hoch)
 *  @param k: Steuerparameter fuer die bewertungsfunktion - stauchung oder streckung der Kurve
 *  @param a: Steuerparameter fuer die Verschiebung auf der x-Achse
 *  @param b: Steuerparameter fuer die Verschiebung auf der y-Aches
 *  @param cheat: Sind tx1 oder tx2 <= 0.0 werden sie zu 1 angenommen

 *  @exceptions: wirft ValueError wenn tx1, oder tx2 kleiner oder gleich 0.0 sind (gibt keine negativen Klicks)

 *  @returns: dict mit den keys 'direction': 1/-1 ; 1 = 'up' , -1 = 'down'
 *                             'score': zahlenwert aus dem Interval
 *                             'infinity': True, wenn z.B. tx2 _wesentlich_ groesser als tx1; sonst False
 *                                 (kann benutzt werden um Anfangssituation/gerade veroeffentlicht zu erkennen)
 */

interface Trend {
  direction: number;
  score: number;
  infinity: boolean;
}

export function getTrend (
  tx1: number,
  tx2: number,
  cheat = false,
  interval = 3,
  k = 4,
  a = -1.3,
  b = 1
): Trend {
  let x = null
  let direction = null

  if (cheat) {
    if (tx1 <= 0.0) {
      tx1 = 1
    }
    if (tx2 <= 0.0) {
      tx2 = 1
    }
  }

  // sicherstellen, dass niemals ne division durch null statt findet
  if (tx1 <= 0.0) {
    throw RangeError(`tx1=${tx1} ist kleiner oder gleich 0.0`)
  }

  if (tx2 <= 0.0) {
    throw RangeError(`tx2=${tx2} ist kleiner oder gleich 0.0`)
  }

  // erzwinge immer werte groesser oder gleich 1 fuer x.
  // wenn tx1 und tx2 gleich gross sind, ist die richtung 'up'
  if (tx1 > tx2) {
    direction = -1
    x = tx1 / tx2
  } else {
    direction = 1
    x = tx2 / tx1
  }

  // die eigentlich Funktion als Latex-code:
  // \frac{\left(\tanh\left(k\left(x+a\right)\right)+b\right)}{2}
  // zum darstellen und ausprobieren den latex-code in https://www.desmos.com/calculator werfen
  // und a,b,k als schieberegler konfigurieren

  const xo = k * (x + a) // stauchen und x-verschiebung
  const fx = Math.tanh(xo) // die eigentlich Funktion
  const y = (fx + b) / 2 // y-verschiebung und auf einen umfang von 1 bringen (zwei Quadranten in einem darstellen)

  // der interval ist linear, kann einfach gerundet werden
  let score = Math.floor(y * interval)

  // catch infinity - eigentlich ist tanh(x) niemals -1 oder 1, aber irgendwann rundet python
  // Beispiel: activityfunction(1000,6000,interval=10,k=4,a=-1.3,b=1) wenn also ein anstieg um 500% statt gefunden hat
  // {'y': 1.0, 'direction': 1, 'x': 6.0, 'interval': 9, 'infinity': True, 'xo': 18.8}
  let infinity = false
  if (Math.floor(fx) === 1 || Math.floor(fx) === -1) {
    // ist dann der maximal wert des Intervals und es wird markiert
    infinity = true
    score = interval - 1
  }

  return {
    direction: direction,
    score: score,
    infinity: infinity
  }
}
