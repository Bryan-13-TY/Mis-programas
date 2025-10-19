public class EjemploPracticaAnalizador {
    public static void main ( String [] args ) {
        int octal1 = /*3.1416*/ -0123 , octal2 = 031 ;
        short dato = 0x12A12 ;
        double PI = 3.1416 , CteGrav = -6.674E-199 ;
        float prom =  ( float ) 0.0 ;
        double val;
        /* Calculos Generales */
        for (int i = 1 ; i < 100 ; i++ ) {
            prom += i ;
        }
        double pot = 7.34E+12 ;
        val = CteGrav * dato * pot ;
        System.out.println ( " Prom = " + ( prom / PI ) + " Result = " + ( val * 0xAB ) ) ;
    }
}