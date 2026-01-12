from views.menu_inicio import menu_inicio
from views.Iniciar_Sesion import inicio_sesion
from views.admin.Admin_menu import AdminVentana
from views.Menu_Principal import Ventana_Principal
from config.iconos import Iconos

if __name__ == "__main__":
    iconos = Iconos()
    app = menu_inicio(iconos=iconos)
    app.run()