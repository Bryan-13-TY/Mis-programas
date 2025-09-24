import java.util.Scanner;

public class ClienteTienda {
    private Scanner sc; // Escaner para cada cliente y solo se accede desde aquí
    private CarritoCompra carrito; // Cada cliente tiene su propio carrito de compra

    public ClienteTienda() { // Clase para cada cliente
        sc = new Scanner(System.in); // Se crea un objeto de tipo Scanner
        carrito = new CarritoCompra();
    }

    public void iniciarMenu() { // Método para inciar el menú del cliente
        int op = 0;

        do  {
            mostrarMenu();
            op = leerOpcion();

            switch (op) {
                case 1:
                    buscarArticulo();
                    break;
                case 2:
                    listarArticulos();
                    break;
                case 3:
                    agregarAlCarrito();
                    break;
                case 4:
                    editarCarrito();
                    break;
                case 5:
                    finalizarCompra();
                    break;
                default:
                    System.out.println(">> ERROR: La opción no es valida");
                    break;
            }
        } while (op != 5);
        
        sc.close();
    }

    private void mostrarMenu() { // Método para mostrar el menú del cliente
        System.out.println("/*------------------.");
        System.out.println("| Tienda: LalitoXDE |");
        System.out.println("`------------------*/");
        System.out.println("\n>> Elije una de las opciones");
        System.out.println("\n1.- Buscar artículos");
        System.out.println("2.- Listar artírculos por tipo");
        System.out.println("3.- Agregar artículos al carrito de compra");
        System.out.println("4.- Editar el contenido del carrito");
        System.out.println("5.- Finalizar compra");
    }

    private int leerOpcion() { // Método para leer la opción
        System.out.print("\nOpción: ");
        return sc.nextInt();
    }

    private void buscarArticulo() { // Método para buscar un artículo
        System.out.println("/*-----------------.");
        System.out.println("| BUSCAR ARTÍCULOS |");
        System.out.println("`-----------------*/");
    }

    private void listarArticulos() { // Método para listar los artículos
        System.out.println("/*-----------------.");
        System.out.println("| LISTAR ARTÍCULOS |");
        System.out.println("`-----------------*/");
    }

    private void agregarAlCarrito() { // Método para agregar un artículo al carrito
        System.out.println("/*-----------------------------.");
        System.out.println("| AGREGAR ARTÍCULOS AL CARRITO |");
        System.out.println("`-----------------------------*/");
    }

    private void editarCarrito() { // Método para editar el carrito de compra
        System.out.println("/*--------------------------------.");
        System.out.println("| EDITAR EL CONTENIDO DEL CARRITO |");
        System.out.println("`--------------------------------*/");
    }

    private void finalizarCompra() { // Método para finalizar la compra
        System.out.println("\n>> La compra ha finalizado con éxito, su comprobante se muestra a continuación:");
    }

    public static void main(String[] args) { // Clase principal
        ClienteTienda cliente = new ClienteTienda(); // Se crea un nevo cliente
        cliente.iniciarMenu(); // Se muestra el menú para el cliente
    }   
}