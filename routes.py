from flask import render_template
from flask_login import current_user

def configure_routes(app):
    @app.route('/ifc-videira')
    def page1():
        place = 'Instituto Federal de Educação Ciência e Tecnologia Catarinense - Campus Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/subway')
    def page2():
        place = 'Subway'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/unoesc')
    def page3():
        place = 'Unoesc Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/hospital-divino-salvador')
    def page4():
        place = 'Hospital Salvatoriano Divino Salvador HSDS'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/aeroporto')
    def page5():
        place = 'Aeroporto de Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/panvel')
    def page6():
        place = 'Panvel Farmácias'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/santtaluz')
    def page7():
        place = 'Santtaluz'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/via-atacadista')
    def page8():
        place = 'Via Atacadista - Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/havan')
    def page9():
        place = 'Havan Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/prefeitura-de-videira')
    def page10():
        place = 'Prefeitura Municipal de Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/viza-atacadista')
    def page11():
        place = 'Viza Atacadista - Videira'
        return render_template('pagamento.html', place=place, username=current_user.username)

    @app.route('/brf')
    def page12():
        place = 'Sociedade Esportiva e Recreativa BRF'
        return render_template('pagamento.html', place=place, username=current_user.username)
