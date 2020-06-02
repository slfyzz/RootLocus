import matplotlib.pyplot as plt
import numpy as np
import math
import sympy as symb
from sympy.solvers import solve
import matplotlib.patches as mpatches


poles = [(-50, -10), (-50, 10), (-25, 0), (0, 0)]
s = symb.Symbol('s')   
Ds = (s**2 + 100 * s + 2600) * s * (s + 25)

#plt.grid(True, which='both')
plt.axhline(y=0, color='0.45')
plt.axvline(x=0, color='0.45')
symb.init_printing(use_unicode=True)

#draw points with label shape and draw line between pairs of points for Ex (0 , 1) then (2, 3) and return those segments
def draw(points, shape, label, link):
    
    x = []
    y = []
    segmentsOfLoci = []
    poles.sort()
    i = 1
    for point in points:
        x.append(point[0])
        y.append(point[1])
        if i % 2 == 0 and point[0] != points[i - 2][0] and link == True:
            plt.plot([point[0], points[i - 2][0]] , [point[1], points[i - 2][1]], "-")
            #print("{point}  to {points[i - 2][0]}")
            segmentsOfLoci.append((points[i - 2][0] ,point[0]))
        i += 1
        
    dots, = plt.plot(x, y, shape, label=label)
    #plt.legend([dots], [label])
    return segmentsOfLoci


def add_patch(legend, label):
    from matplotlib.patches import Patch
    ax = legend.axes

    handles, labels = ax.get_legend_handles_labels()
    handles.append(Patch(facecolor='white', edgecolor='w'))
    labels.append(label)

    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())



#return the sum of pairs that are in the real axis
def sumOf(arr):
    
    if arr is None:
        return 0;
    else:
        sum = 0
        for item in arr:
            sum += item[0]
        return sum;

def drawLineByAngle(point, angle, length, color, line):
     
     x = [point[0], point[0] + length * math.cos(math.radians(angle))]
     y = [point[1], point[1] + length * math.sin(math.radians(angle))]
     
     plt.plot(x, y, line + color)
     
def drawDottedLines(sigma, theta):
    
    angle = theta
    r = 1
    while True:
        drawLineByAngle((sigma, 0), angle, 100, "r", "--")
        #print(f'{angle} from {sigma}')
        r += 2
        angle = (theta * r) % 360
        if angle == theta:
            break 
    
def drawAngleOfDept(point, poles):
    
    angle = 180
    for pole in poles:
        if pole == point:
            continue
        angle -= math.degrees(math.atan2((point[1] - pole[1]), (point[0] - pole[0])))
        print(f"{angle}   {pole}")
    
    drawLineByAngle(point, angle, 5, "b", "--")
    drawLineByAngle(point, 0, 5, "b", "--")
    plt.text(point[0] + 1, point[1] + 1, 'θ', fontsize=10)
     
    drawLineByAngle((point[0], point[1] * -1), angle * -1, 5, "b", "--")
    drawLineByAngle((point[0], point[1] * -1), 0 , 5, "b", "--")
    plt.text(point[0] + 1, point[1] * -1 - 4, 'θ', fontsize=10)
    
    if angle < 0:
        angle += 360
    return round(angle, 5)
             
    
    

def rootLocus():
    
    segmentsOfLoci = draw(poles, "x", "poles", True)
    
    # get both sum of poles and zeros
    sumOfPoles = sumOf(poles)
    sumOfZeros = 0 #theres no zeros 
    q = len(poles)
    
    sigma = (sumOfPoles - sumOfZeros) / q
    theta = 180 / q
    drawDottedLines(sigma, theta)
    

    DsDash = symb.simplify(symb.diff(Ds, s))
    DsDashCoeff = symb.Poly(DsDash, s).coeffs()
    roots = np.roots(DsDashCoeff)
    roots = roots[np.isreal(roots)]
    for seg in segmentsOfLoci:
        for root in roots:
            if root >= seg[0] and root <= seg[1]:
                draw([(root, 0)], "s", " break away points", False)
    
    #by using Routh 
    interWithImgAxis = [(0, 2 * math.sqrt(130)) , (0, -2 * math.sqrt(130))]
    draw(interWithImgAxis, "v", "intersections with the imaginary axis", False)
    angle = drawAngleOfDept((-50 , 10), poles)
    
    return Ds, angle
    
    
    
def drawExactRoots(func=Ds):
    k = np.linspace(0, 100000000, 15000)
    #print(k)
    #print(symb.Poly(func + 2, s).coeffs())
    real = []
    img = []
    for num in k:
        simp = symb.Poly(func + num, s).coeffs()
        #print(symb.Poly(func + num, s).coeffs())
        roots = np.roots(simp)
        for root in roots:
            real.append(root.real)
            img.append(root.imag)
            
    #print(real)
    #print(img)
    plt.plot(real, img, ".",label="Exact Curve")    

    


if __name__ == "__main__":
    drawExactRoots()
    func ,angle = rootLocus()
    add_patch(plt.legend(loc='lower right'), f'θ is {angle}')
    plt.show()
    