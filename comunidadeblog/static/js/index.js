// Função para exibir o modal de confirmação
function exibirModal() {
  var modal = document.getElementById("modal-confirmacao");
  modal.style.display = "block";
}

// Função para fechar o modal
function fecharModal() {
  var modal = document.getElementById("modal-confirmacao");
  modal.style.display = "none";
}

// Função para realizar a exclusão
function excluirItem() {
  // Lógica para excluir o item aqui
  // alert("Item excluído com sucesso!");
  fecharModal();
}