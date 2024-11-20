
import com.sun.jna.Library;
import com.sun.jna.Native;


public interface C extends Library {
    C INSTANCE = (C) Native.load("ruta/a/tu/bibliotecaC", C.class);

    void ejecutarCodigo(String codigoC);
}