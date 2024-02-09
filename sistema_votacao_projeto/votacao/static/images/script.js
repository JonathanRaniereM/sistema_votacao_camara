




function toggleMenu() {
    var menu = document.querySelector('.menu');
    menu.classList.toggle('active');
}


function toggleSubmenu(id) {
    var submenu = document.getElementById(id);
    var icon = submenu.previousElementSibling.querySelector('.icon-expand');

    submenu.classList.toggle('active');

    if (submenu.classList.contains('active')) {
        icon.classList.add('icon-minus');
        icon.classList.remove('icon-plus');
        icon.innerHTML = '-';
    } else {
        icon.classList.add('icon-plus');
        icon.classList.remove('icon-minus');
        icon.innerHTML = '+';
    }
}

var menuHeaders = document.querySelectorAll('.menu-header');

menuHeaders.forEach(function(header) {
    header.addEventListener('click', function() {
        // Se o cabeçalho clicado já tiver a classe 'active', remova-a
        if(header.classList.contains('active')) {
            header.classList.remove('active');
        } else {
            // Caso contrário, remova a classe 'active' de todos os cabeçalhos
            menuHeaders.forEach(function(innerHeader) {
                innerHeader.classList.remove('active');
            });

            // E adicione a classe 'active' ao cabeçalho clicado
            header.classList.add('active');
        }
    });
});

//SUBMENU DIREITO HEADER
function toggleMenu() {
    $(".custom-select").toggle(); // Simplesmente alternar a exibição do menu
}

$(document).ready(function() {
    $(".option").click(function() {
        var selected = $(this).html();
        $(this).closest(".custom-select").find(".selected-option").html(selected);
        $(this).closest(".options").hide();
    });
});



document.addEventListener('DOMContentLoaded', function() {
    function showContent(contentId) {
        console.log(`Showing content for ${contentId}`); // Log para depuração
        // Oculta todas as seções
        document.querySelectorAll('.subitem-content').forEach(function(content) {
            content.style.display = 'none';
        });
        
        // Mostra apenas a seção correspondente
        var contentElement = document.getElementById(contentId + '-content');
        console.log('Content element:', contentElement); // Log para depuração
        contentElement.style.display = 'block'; // ESSA É A LINHA 74
    }

    var currentView = "{{ view }}";  // Pega a variável view do Django
    
    if (currentView === 'parlamentar'){
    document.getElementById('parlamentar-link').addEventListener('click', function(event) { //ESSA É A LINHA 84
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('parlamentar');
    })};


    if (currentView === 'partido_politico'){
    document.getElementById('partido-politico-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('partido-politico');
        //window.location.hash = 'partido-politico';
    })};
 

    //TERMINAR DE MUDAR ESSES ABAIXO PARA FICAR IGUAL OS DOIS PRIMEIROS
    document.getElementById('mesa-diretora-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('mesa-diretora');
    });

    document.getElementById('parametros-de-votacao-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('parametros-de-votacao');
    });

    document.getElementById('tipo-de-acao-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('tipo-de-acao');
    });

    
    document.getElementById('sessao-plenario-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('sessao-plenario');
    });

    document.getElementById('votacao-plenario-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('votacao-plenario');
    });

    document.getElementById('painel-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('painel');
    });

    document.getElementById('cenario-painel-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('cenario-painel');
    });

    document.getElementById('buzina-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('buzina');
    });

    document.getElementById('relatorio-de-presenca-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('relatorio-de-presenca');
    });

    document.getElementById('relatorio-de-votacao-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('relatorio-de-votacao');
    });

    document.getElementById('relatorio-geral-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('relatorio-geral');
    });

    document.getElementById('perfil-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('perfil');
    });

    document.getElementById('usuario-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('usuario');
    });

    document.getElementById('cores-do-painel-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        showContent('cores-do-painel');
    });
});


$(document).ready(function() {
    // Logic for "Imprimir Ausentes (Apenas Plenário)" switch
    $("#fa-switch-ausentes").change(function() {
        if ($(this).is(':checked')) {
            $("#on-icon-ausentes").show();
            $("#off-icon-ausentes").hide();
        } else {
            $("#off-icon-ausentes").show();
            $("#on-icon-ausentes").hide();
        }
    });

    // Logic for "Imprimir Recomposições (Apenas Plenário)" switch
    $("#fa-switch-recomposicoes").change(function() {
        if ($(this).is(':checked')) {
            $("#on-icon-recomposicoes").show();
            $("#off-icon-recomposicoes").hide();
        } else {
            $("#off-icon-recomposicoes").show();
            $("#on-icon-recomposicoes").hide();
        }
    });

    $("#fa-switch-nao-votantes").change(function() {
        if ($(this).is(':checked')) {
            $("#on-icon-nao-votantes").show();
            $("#off-icon-nao-votantes").hide();
        } else {
            $("#off-icon-nao-votantes").show();
            $("#on-icon-nao-votantes").hide();
        }
    });
});


function displayImage(input) {
    var cameraIcon = document.getElementById('cameraIcon');
    var imageElement = document.getElementById('displayedImg');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            imageElement.src = e.target.result;
            cameraIcon.style.opacity = '0'; // Esconde o ícone da câmera quando uma imagem é selecionada
        }

        reader.readAsDataURL(input.files[0]);
    } else {
        imageElement.src = "";
        cameraIcon.style.opacity = '1';  // Mostra o ícone da câmera se nenhuma imagem estiver selecionada
    }
}
function triggerFileClick() {
    document.getElementById('profileImage').click();
}


function voltarFunctionNovo() {
    document.getElementById("cadastro-form").style.display = "none"; // Oculta o formulário
    document.getElementById("parlamentar-table").style.display = "block"; // Mostra a tabela
    document.getElementById("search-input-parlamentar").style.display = "block"; // Mostrar input
    document.getElementById("novo_parlamentar").style.display = "inline"; // Mostra botao
    document.getElementById("pesquisa_parlamentar").style.display = "inline"; // Mostra pesquisa
}

function voltarFunctionEditar() {
    // Esconde o formulário de edição:
    document.getElementById('cadastro-form').style.display = 'none';
    
    // Mostra os outros elementos:
    document.getElementById('parlamentar-table').style.display = 'block';
    document.querySelector('.search-bar').style.display = 'block';
    document.getElementById('pesquisa_parlamentar').style.display = 'block';
    document.getElementById('novo_parlamentar').style.display = 'block';
}

function decideVoltarFunction() {
    var context = document.getElementById('voltar_parlamentar').getAttribute('data-context');
    if (context === 'edit') {
        voltarFunctionEditar();
    } else {
        voltarFunctionNovo();
    }
}


function voltarPartidosFunction() {
    document.getElementById("partido-form").style.display = "none"; // Oculta o formulário
    document.getElementById("partido-table").style.display = "block"; // Mostra a tabela
    document.getElementById("search-input-partido").style.display = "block"; // Mostrar input
    document.getElementById("botao-novo").style.display = "inline"; // Mostra botao
    document.getElementById("pesquisa_partido").style.display = "inline"; // Mostra pesquisa
}

function voltarMesaFunction() {
    document.getElementById("mesa-form").style.display = "none"; // Oculta o formulário
    document.getElementById("mesa-table").style.display = "block"; // Mostra a tabela
    document.getElementById("search-input-mesa").style.display = "block"; // Mostrar input
    document.getElementById("botao-novo-mesa").style.display = "inline"; // Mostra botao
    document.getElementById("pesquisa_mesa").style.display = "inline"; // Mostra pesquisa
}

function salvarParlamentarFunction(event) {
    event.preventDefault();
    var modal = document.getElementById("successModalParlamentar");
    modal.style.display = "block";
}

function salvarPartidoFunction(event) {
    event.preventDefault();
    var modal = document.getElementById("successModalPartido");
    modal.style.display = "block";
}

function salvarMesaFunction(event) {
    event.preventDefault();
    var modal = document.getElementById("successModalMesa");
    modal.style.display = "block";
}

function closeModal(modalOrId) {
    var modal;

    if (typeof modalOrId === "string") {
        modal = document.getElementById(modalOrId);
    } else {
        modal = modalOrId;
    }

    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        closeModal(event.target);
    }
}

var spans = document.getElementsByClassName("close-button");
for (var i = 0; i < spans.length; i++) {
    spans[i].onclick = function() {
        closeModal(this.parentElement.parentElement);
    }
}

//FUNÇÃO DE BARRA DE PESQUISA PARLAMENTAR
document.addEventListener("DOMContentLoaded", function() {

    const input = document.getElementById('search-input-parlamentar');

    input.addEventListener('keyup', function() {
        let filter = input.value.toUpperCase();
        let table = document.querySelector("#parlamentar-table table");
        let trs = table.getElementsByTagName('tr');

        // Filtrar linhas baseado no input
        for (let i = 1; i < trs.length; i++) {
            let td = trs[i].getElementsByTagName('td')[0];
            if (td) {
                let txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    trs[i].style.display = "";
                } else {
                    trs[i].style.display = "none";
                }
            }
        }

        // Resetar os estilos de cor sim, cor não para as linhas visíveis
        let visibleRows = 0;
        for (let i = 1; i < trs.length; i++) {
            if (trs[i].style.display !== "none") {
                if (visibleRows % 2 === 0) {
                    trs[i].style.backgroundColor = "#e6e6e6"; // Cor para linhas pares
                } else {
                    trs[i].style.backgroundColor = "#f2f2f2"; // Cor para linhas ímpares
                }
                visibleRows++;
            }
        }
    });

});




 /* MOSTRAR FORM DE NOVO PARLAMENTAR */
function showForm() {
    const form = document.getElementById('cadastro-form');
    document.querySelector('input[name="vereador_id"]').value = '';
    const table = document.getElementById('parlamentar-table');
    document.getElementById('voltar_parlamentar').setAttribute('data-context', 'new');
    const campoPesquisa = document.getElementById('search-input-parlamentar');
    const botaoPesquisa = document.querySelector('.search-button');
    const botaoNovoParlamentar = document.getElementById('novo_parlamentar');
    
    // Limpar os campos do formulário:
    document.getElementById('name').value = '';
    document.getElementById('parlamentar').value = '';
    document.getElementById('birthdate').value = '';          // Limpando o campo de data de nascimento
    document.getElementById('gender').selectedIndex = 0;               // Resetando o dropdown de sexo
    document.getElementById('profileImage').value = '';              // Limpando o campo de arquivo de imagem
    const displayedImg = document.getElementById('displayedImg');    // Obtendo a referência para a imagem exibida
    displayedImg.src = '';                                           // Removendo a imagem atual                       
    document.querySelector('.fa-camera').style.opacity = '1';        // Mostrando o ícone da câmera novamente
    
    form.style.display = 'block';
    table.style.display = 'none';
    campoPesquisa.style.display = 'none';
    botaoPesquisa.style.display = 'none';
    botaoNovoParlamentar.style.display = 'none';
}


function deleteVereador(vereadorId) {
    if (confirm("Tem certeza que deseja excluir este vereador?")) {
        $.ajax({
            url: '/home/configuracao/',  // Modifique o caminho para a sua URL correta
            type: 'POST',
            data: {
                'vereador_id': vereadorId,
                'action': 'delete',
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.status == 'success') {
                    // Recarregar a página
                    location.reload();  // Simples recarga de página
                } else {
                    alert("Erro ao excluir o vereador!");
                }
            },
            error: function(err) {
                // Tratar o erro aqui
                console.error(err);
                alert("Erro ao excluir o vereador!");
            }
        });
    }
}

//INICIO DA FUNÇÃO EDITARPARLAMENTAR

function editVereador(vereadorId, nomeVereador, nomeCompleto, dataNascimento, sexo, imageUrl) {
    // Preencha o input hidden com o ID do vereador
    document.querySelector('input[name="vereador_id"]').value = vereadorId;

    // Preencher o formulário com os detalhes do vereador usando os IDs
    document.getElementById('parlamentar').value = nomeVereador;
    document.getElementById('name').value = nomeCompleto;
    
    // Convertendo a string de data para o formato "YYYY-MM-DD"
    let dateParts = new Date(dataNascimento).toISOString().split("T")[0];
    document.getElementById('birthdate').value = dateParts;

    // Para o dropdown do sexo
    var sexoSelect = document.getElementById('gender');
    for (var i = 0; i < sexoSelect.options.length; i++) {
        if (sexoSelect.options[i].value === sexo) {
            sexoSelect.options[i].selected = true;
            break;
        }
    }

    // Atualizar a imagem do vereador
    var imageElement = document.getElementById('displayedImg');
    if (imageUrl && imageUrl !== 'undefined') {
        imageElement.src = imageUrl;
        imageElement.style.display = 'block'; // Mostra a imagem se a URL for fornecida
        cameraIcon.style.opacity = '0';  // Esconde o ícone da câmera
    } else {
        imageElement.style.display = 'none';  // Esconde se não houver imagem
        cameraIcon.style.opacity = '1';  // Mostra o ícone da câmera
    }

    // Atualizar o comportamento dos botões/elementos como na implementação antiga
    document.getElementById('voltar_parlamentar').setAttribute('data-context', 'edit');
    document.getElementById('cadastro-form').style.display = 'block';
    document.getElementById('parlamentar-table').style.display = 'none';
    document.querySelector('.search-bar').style.display = 'none';
    document.getElementById('pesquisa_parlamentar').style.display = 'none';
    document.getElementById('novo_parlamentar').style.display = 'none';

    console.log(dataNascimento); // deve imprimir algo como "1990-05-25"
    console.log(sexo); // deve imprimir o valor esperado, como "masculino" ou "feminino" ou qualquer valor que você tenha nas opções do dropdown.
    console.log(imageUrl)

}

document.addEventListener("DOMContentLoaded", function () {
    const editLinks = document.querySelectorAll(".edit-link");

    editLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Impede o comportamento padrão de navegação

            // Captura o ID e os outros atributos data- do botão clicado
            const vereadorId = link.getAttribute("data-vereador-id");
            const nomeVereador = link.getAttribute("data-vereador-nome");
            const nomeCompleto = link.getAttribute("data-nome-completo");
            const dataNascimento = link.getAttribute("data-data-nascimento");
            const sexo = link.getAttribute("data-sexo");
            const imageUrl = link.getAttribute("data-image");

            // Chama a função editVereador
            editVereador(vereadorId, nomeVereador, nomeCompleto, dataNascimento, sexo,imageUrl);
        });
    });
});
//FIM DA FUNÇÃO EDITARPARLAMENTAR


/* MOSTRAR FORM DE NOVO PARTIDO */
const botaoNovo = document.getElementById('botao-novo');
const formPartido = document.getElementById('partido-form');
const tabelaPartidos = document.getElementById('partido-table');
const campoPesquisaPartido = document.getElementById('search-input-partido');
const botaoPesquisaPartido = document.getElementById('pesquisa_partido');

botaoNovo.addEventListener('click', () => {
    formPartido.style.display = 'block'; // Mostra o formulário
    tabelaPartidos.style.display = 'none'; // Oculta a tabela
    campoPesquisaPartido.style.display = 'none'; // Oculta o campo de pesquisa
    botaoPesquisaPartido.style.display = 'none'; // Oculta o botão de pesquisa
    botaoNovo.style.display = 'none'; // Oculta o campo de pesquisa

});







/* MOSTRAR FORM DE NOVA MESA */
const botaoNovoMesa = document.getElementById('botao-novo-mesa');
const formMesa = document.getElementById('mesa-form');
const tabelaMesa = document.getElementById('mesa-table');
const campoPesquisaMesa = document.getElementById('search-input-mesa');
const botaoPesquisaMesa = document.getElementById('pesquisa_mesa'); 

botaoNovoMesa.addEventListener('click', () => {
    formMesa.style.display = 'block'; // Mostra o formulário
    tabelaMesa.style.display = 'none'; // Oculta a tabela
    campoPesquisaMesa.style.display = 'none'; // Oculta o campo de pesquisa
    botaoPesquisaMesa.style.display = 'none'; // Oculta o botão de pesquisa
    botaoNovoMesa.style.display = 'none';
});


function displayImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            const displayedImg = document.getElementById('displayedImg');
            displayedImg.src = e.target.result;
            
            // Esconde o ícone da câmera
            const cameraIcon = displayedImg.parentElement.querySelector('.fa-camera');
            cameraIcon.style.display = 'none';
        }

        reader.readAsDataURL(input.files[0]);
    }
}

