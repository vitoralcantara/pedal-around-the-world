==========
Decorators
==========

---
rtr
---

^^^^^^^^^^^^^^
Pra Que Serve?
^^^^^^^^^^^^^^

É uma abstração do ``render_to_response``, com 2 principais características:
 * A função decorada deve retornar um dicionário
 * Retira a obrigação de informar qual template deve ser renderizado.
 * Já adiciona ``django.templateRequestContext`` ao contexto

^^^^^^^^^^
Como Usar?
^^^^^^^^^^

Definindo que template renderizar::

	@rtr('meu_template.html')
	def foo(request):
	    return dict(nome='tulio')

Deixando que o rtr descubra que template renderizar::

	@rtr()
	def foo(request):
	    return dict(nome='tulio')

O trecho de código acima tem o mesmo efeito que::

	def foo(request):
	    return render_to_response('<app_label>/foo.html', dict(name='tulio'),
	        context_instance=RequestContext(request))

Note que ``<<app_label>>`` é o nome da aplicação que contém a função ``foo``.

--------------
permission_required (Não implementado)
--------------

^^^^^^^^^^^^^^
Pra Que Serve?
^^^^^^^^^^^^^^

blah

^^^^^^^^^^
Como Usar?
^^^^^^^^^^

bleh