
from botcity.core import DesktopBot

class Bot(DesktopBot):
    def action(self, execution=None):
    
        # Entrar no site e fazer o registro
          
        self.browse("https://automationexercise.com/login")
        if not self.find( "name", matching=0.97, waiting_time=10000):
            self.not_found("name")
        self.click()
        self.paste("Luan Pinheiro")
        if not self.find( "email", matching=0.97, waiting_time=10000):
            self.not_found("email")
        self.click()
        self.paste("luan@gmail.com")
        if not self.find( "signup", matching=0.97, waiting_time=10000):
            self.not_found("signup")
        self.click()
        
        # Cadastrar dados do usuario
          
        if not self.find( "sexo", matching=0.97, waiting_time=10000):
            self.not_found("sexo")
        self.click()
        if not self.find( "senha", matching=0.97, waiting_time=10000):
            self.not_found("senha")
        self.click()
        self.paste("12345678")
        self.scroll_down(900)
        if not self.find( "primeiro.nome", matching=0.97, waiting_time=10000):
            self.not_found("primeiro.nome")
        self.click()
        self.paste("Luan")
        if not self.find( "sobrenome", matching=0.97, waiting_time=10000):
            self.not_found("sobrenome")
        self.click()
        self.paste("Pinheiro")
        if not self.find( "endereco", matching=0.97, waiting_time=10000):
            self.not_found("endereco")
        self.click()
        self.paste("Rua Qualquer, 555")
        if not self.find( "estado", matching=0.97, waiting_time=10000):
            self.not_found("estado")
        self.click()
        self.paste("Rajastão")
        self.scroll_down(400)
        if not self.find( "cidade", matching=0.97, waiting_time=10000):
            self.not_found("cidade")
        self.click()
        self.paste("Jaipur")
        if not self.find( "codigo.area", matching=0.97, waiting_time=10000):
            self.not_found("codigo.area")
        self.click()
        self.paste("55")
        if not self.find( "telefone", matching=0.97, waiting_time=10000):
            self.not_found("telefone")
        self.click()
        self.paste("4002-8922")
        if not self.find( "criar", matching=0.97, waiting_time=10000):
            self.not_found("criar")
        self.click()
        if not self.find( "continue", matching=0.97, waiting_time=10000):
            self.not_found("continue")
        self.click()
        self.wait(1000)
        
        #Efetuar compra 
         
        if not self.find( "pag.carregou", matching=0.97, waiting_time=10000):
            self.not_found("pag.carregou")
        self.wait(1000)
        self.scroll_down(700)
        if not self.find( "fechar", matching=0.97, waiting_time=10000):
            self.not_found("fechar")
        self.click()
        self.scroll_down(700)
        if not self.find( "carrinho", matching=0.97, waiting_time=10000):
            self.not_found("carrinho")
        self.click()
        if not self.find( "abrir.compra", matching=0.97, waiting_time=10000):
            self.not_found("abrir.compra")
        self.click()
        if not self.find( "continuar.compra", matching=0.97, waiting_time=10000):
            self.not_found("continuar.compra")
        self.click()
        if not self.find( "carregou.pag", matching=0.97, waiting_time=10000):
            self.not_found("carregou.pag")
        self.scroll_down(1000)  
        if not self.find( "fazer.pedido", matching=0.97, waiting_time=10000):
            self.not_found("fazer.pedido")
        self.click()
        if not self.find( "cartao", matching=0.97, waiting_time=10000):
            self.not_found("cartao")
        self.click()
        self.paste("Luan Pinheiro")
        if not self.find( "numero.cartao", matching=0.97, waiting_time=10000):
            self.not_found("numero.cartao")
        self.click()
        self.paste("1234567890")
        if not self.find( "cvc", matching=0.97, waiting_time=10000):
            self.not_found("cvc")
        self.click()
        self.paste("123")
        if not self.find( "mm", matching=0.97, waiting_time=10000):
            self.not_found("mm")
        self.click()
        self.paste("11")
        if not self.find( "yyyy", matching=0.97, waiting_time=10000):
            self.not_found("yyyy")
        self.click()
        self.paste("2025")
        if not self.find( "confirmar", matching=0.97, waiting_time=10000):
            self.not_found("confirmar")
        self.click()
        if not self.find( "comprovante", matching=0.97, waiting_time=10000):
            self.not_found("comprovante")
        self.click()
        if not self.find( "comprovantetxt", matching=0.97, waiting_time=10000):
            self.not_found("comprovantetxt")
        self.click()
        
        
        
        
              
        
        

        
        
        
        
        
        
        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()

