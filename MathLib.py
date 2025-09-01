class MathLib:

    def reflectVector(normal, direction):
        #R=I−2(I⋅N)
        reflect = 2 * np.dot(normal, direction) 
        reflect = np.multiply(reflect, normal)
        reflect = np.subtract(reflect, direction)
        reflect /= np.linalg.norm(reflect)
        return reflect
