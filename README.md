#    Anizotropná segmentácia obrazu pomocou tenzora gradientovej štruktúry
 
# Čo je tenzor gradientovej štruktúry:

V matematike je tenzor gradientovej štruktúry (tiež označovaný ako matica druhého momentu, tenzor momentu druhého rádu, tenzor zotrvačnosti atď.) matica odvodená z gradientu funkcie. Sumarizuje dominantné smery gradientu v určenom susedstve bodu a stupeň, v akom sú tieto smery koherentné (koherentnosť). Tenzor gradientovej štruktúry sa široko používa v spracovaní obrazu a počítačovom videní pre segmentáciu 2D / 3D obrazu, detekciu pohybu, adaptívnu filtráciu, lokálnu detekciu obrazových prvkov atď.

Medzi dôležité vlastnosti anizotropných obrazov patrí orientácia a koherencia lokálnej anizotropie. V tomto článku ukážeme, ako odhadnúť orientáciu a koherenciu a ako segmentovať anizotropný obraz s jednou lokálnou orientáciou tenzorom gradientnej štruktúry.

Tenzor gradientovej štruktúry obrazu je symetrická matica 2x2. Vlastné vektory tenzora gradientovej štruktúry naznačujú lokálnu orientáciu, zatiaľ čo vlastné hodnoty dávajú koherenciu (miera anizotropismu).

Tenzor gradientovej štruktúry J, ktorý pochádza zo Z (náhodný obrázok), môže byť zapísaný ako:


J=[■(J_11&J_12@J_12&J_22 )]


Kde J_11=M[Z_x^2 ], J_22=M[Z_y^2 ], J_12=M[Z_x Z_y ] - komponenty tenzora, M[] je symbolom matematického očakávania (túto operáciu môžeme považovať za priemernú hodnotu v okne w), Z_xa Z_y sú čiastkové derivácie obrazu Z vzhľadom na x a y.

Vlastné hodnoty tenzora možno nájsť v nasledujúcom vzorci:

λ_1,2=J_11+J_22±√((J_11-J_22 )^2+4J_12^2 )

Kde λ_1 je najväčšia vlastná hodnota a λ_2 je najmenšia vlastná hodnota.
Ako odhadnúť orientáciu a koherenciu anizotropného obrazu pomocou tenzora gradientovej štruktúry?
Orientácia anizotropného obrazu: 
α=0.5arctg (2J_12)/(J_22-J_11 )

Koherencia:
C=(λ_1-λ_2)/(λ_1+λ_2 )

Koherencia sa pohybuje od 0 do 1. Pre ideálnu miestnu orientáciu (λ_2=0 , λ_1>0) je jedna, pre štruktúru izotropnej šedej hodnoty (λ_1=λ_2>0) je nula.

# Pseudokod:
....

# Literatura:
https://docs.opencv.org/master/d4/d70/tutorial_anisotropic_image_segmentation_by_a_gst.html
