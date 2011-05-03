from abjad.components import Staff
from abjad.tools import componenttools


def get_first_staff_in_improper_parentage_of_component(component):
   r'''.. versionadded:: 1.1.2

   Get first staff in improper parentage of `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }

   ::

      abjad> stafftools.get_first_staff_in_improper_parentage_of_component(staff[1])
      Staff{4}

   Return staff or none.
   '''

   return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      component, Staff)
