# -*- encoding: utf-8 -*-
import os
import subprocess
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class ScoreManager(ScoreManagerObject):
    r'''Score manager.

    ::

        >>> score_manager = scoremanager.core.ScoreManager()
        >>> score_manager
        ScoreManager()

    Returns score manager.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        ScoreManagerObject.__init__(self, session=session)
        self.session._score_manager = self
        self._segment_package_wrangler = \
            wranglers.SegmentPackageWrangler(session=self.session)
        self._material_package_manager_wrangler = \
            wranglers.MaterialPackageManagerWrangler(session=self.session)
        self._material_package_wrangler = \
            wranglers.MaterialPackageWrangler(session=self.session)
        self._score_package_wrangler = \
            wranglers.ScorePackageWrangler(session=self.session)
        self._stylesheet_file_wrangler = \
            wranglers.StylesheetFileWrangler(session=self.session)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'score manager'

    @property
    def _score_status_string(self):
        return '{} scores'.format(self.session.scores_to_show)

    ### PRIVATE METHODS ###

    def _get_next_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self.session.current_score_snake_case_name is None:
            return score_package_names[0]
        index = score_package_names.index(
            self.session.current_score_snake_case_name)
        next_index = (index + 1) % len(score_package_names)
        return score_package_names[next_index]

    def _get_previous_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self.session.current_score_snake_case_name is None:
            return score_package_names[-1]
        index = score_package_names.index(
            self.session.current_score_snake_case_name)
        prev_index = (index - 1) % len(score_package_names)
        return score_package_names[prev_index]

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            wrangler = self.score_package_wrangler
            if result in wrangler.list_visible_asset_packagesystem_paths():
                self.interactively_edit_score(result)

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        section = menu.make_command_section()
        section.append(('scores - new', 'new'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('cache - view', 'cv'))
        section.append(('cache - write', 'cw'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('library - manage materials', 'lmm'))
        section.append(('library - manage stylesheets', 'lmy'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('scores - show all', 'ssl'))
        section.append(('scores - show active', 'ssv'))
        section.append(('scores - show mothballed', 'ssmb'))
        menu._make_default_hidden_sections()
        return menu

    def _make_score_selection_menu(self):
        wrangler = self.score_package_wrangler
        if self.session.is_first_run:
            #print 'FIRST!'
            menu_entries = self.session.io_manager._read_cache()
            if not menu_entries:
                self.session.io_manager._write_cache()
                menu_entries = wrangler._make_asset_menu_entries()
            self.session.is_first_run = False
        else:
            #print 'NOT FIRST!'
            menu_entries = wrangler._make_asset_menu_entries()
        if not self.session.show_example_scores:
            menu_entries = self._remove_example_score_menu_entries(
                menu_entries)
        menu = self.session.io_manager.make_menu(
            where=self._where,
            include_default_hidden_sections=False,
            )
        asset_section = menu.make_asset_section()
        asset_section.menu_entries = menu_entries
        return menu

    def _remove_example_score_menu_entries(self, menu_entries):
        result = []
        for menu_entry in menu_entries:
            if 'Example Score' in menu_entry[0]:
                continue
            result.append(menu_entry)
        return result

    def _run(
        self, 
        pending_user_input=None, 
        clear=True, 
        cache=False, 
        is_test=False, 
        dump_transcript=False,
        show_example_scores=True,
        ):
        type(self).__init__(self)
        self.session._push_controller(self)
        self.session.io_manager._assign_user_input(
            pending_user_input=pending_user_input,
            )
        self.session._cache_breadcrumbs(cache=cache)
        self.session._push_breadcrumb(self._breadcrumb)
        if is_test:
            self.session.is_test = True
        self.session.dump_transcript = dump_transcript
        self.session.show_example_scores = show_example_scores
        run_main_menu = True
        while True:
            self.session._push_breadcrumb(self._score_status_string)
            if run_main_menu:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
            else:
                run_main_menu = True
            if self.session._backtrack(source='home'):
                self.session._pop_breadcrumb()
                self.session._clean_up()
                break
            elif self.session.is_navigating_to_next_score:
                self.session.is_navigating_to_next_score = False
                self.session.is_backtracking_to_score_manager = False
                result = self._get_next_score_package_name()
            elif self.session.is_navigating_to_previous_score:
                self.session.is_navigating_to_previous_score = False
                self.session.is_backtracking_to_score_manager = False
                result = self._get_previous_score_package_name()
            elif not result:
                self.session._pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self.session._backtrack(source='home'):
                self.session._pop_breadcrumb()
                self.session._clean_up()
                break
            elif self.session.is_navigating_to_sibling_score:
                run_main_menu = False
            self.session._pop_breadcrumb()
        self.session._pop_controller()
        self.session._pop_breadcrumb()
        self.session._restore_breadcrumbs(cache=cache)

    ### PUBLIC PROPERTIES ###

    @property
    def material_package_manager_wrangler(self):
        r'''Score manager material package maker wrangler:

        ::

            >>> score_manager.material_package_manager_wrangler
            MaterialPackageManagerWrangler()

        Returns material package maker wrangler.
        '''
        return self._material_package_manager_wrangler

    @property
    def material_package_wrangler(self):
        r'''Score manager material package wrangler:

        ::

            >>> score_manager.material_package_wrangler
            MaterialPackageWrangler()

        Returns material package wrangler.
        '''
        return self._material_package_wrangler

    @property
    def score_package_wrangler(self):
        r'''Score manager score package wrangler:

        ::

            >>> score_manager.score_package_wrangler
            ScorePackageWrangler()

        Returns score package wrangler.
        '''
        return self._score_package_wrangler

    @property
    def segment_package_wrangler(self):
        r'''Score manager segment package wrangler:

        ::

            >>> score_manager.segment_package_wrangler
            SegmentPackageWrangler()

        Returns segment package wrangler.
        '''
        return self._segment_package_wrangler

    @property
    def stylesheet_file_wrangler(self):
        r'''Score manager stylesheet file wrangler:

        ::

            >>> score_manager.stylesheet_file_wrangler
            StylesheetFileWrangler()

        Returns stylesheet file wrangler.
        '''
        return self._stylesheet_file_wrangler

    ### PUBLIC METHODS ###

    def display_active_scores(self):
        self.session.display_active_scores()

    def display_all_scores(self):
        self.session.display_all_scores()

    def display_mothballed_scores(self):
        self.session.display_mothballed_scores()

    def interactively_edit_score(self, score_package_path):
        manager = self.score_package_wrangler._initialize_asset_manager(
            score_package_path)
        score_package_name = score_package_path.split('.')[-1]
        manager.session.current_score_snake_case_name = score_package_name
        manager._run(cache=True)
        self.session.current_score_snake_case_name = None

    def interactively_make_new_score(self):
        self.score_package_wrangler.interactively_make_asset(rollback=True)

    def interactively_run_doctest(self, prompt=True):
        path = self.configuration.user_score_packages_directory_path
        command = 'ajv doctest {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self.session.io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self.session.io_manager.proceed(prompt=prompt)

    def interactively_run_pytest(self, prompt=True):
        path = self.configuration.user_score_packages_directory_path
        command = 'py.test -rf {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self.session.io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self.session.io_manager.proceed(prompt=prompt)

    def manage_materials(self):
        self.material_package_wrangler._run(
            rollback=True, 
            head=self.configuration.built_in_material_packages_package_path,
            )

    def manage_stylesheets(self):
        self.stylesheet_file_wrangler._run(
            rollback=True, 
            )

    def repository_add_assets(self, prompt=True):
        self.score_package_wrangler.repository_add_assets()

    def repository_ci_assets(self, prompt=True):
        self.score_package_wrangler.repository_ci_assets()

    def repository_st_assets(self, prompt=True):
        self.score_package_wrangler.repository_st_assets()

    def repository_up_assets(self, prompt=True):
        self.score_package_wrangler.repository_up_assets()

    def view_cache(self):
        file_path = self.configuration.cache_file_path
        if os.path.isfile(file_path):
            command = 'vi -R {}'.format(file_path)
            self.session.io_manager.spawn_subprocess(command)

    def write_cache(self, prompt=True):
        self.session.io_manager._write_cache(prompt=prompt)

    ### UI MANIFEST ###

    user_input_to_action = {
        'cv': view_cache,
        'cw': write_cache,
        'lmm': manage_materials,
        'new': interactively_make_new_score,
        'radd': repository_add_assets,
        'rci': repository_ci_assets,
        'rst': repository_st_assets,
        'rup': repository_up_assets,
        'ssl': display_all_scores,
        'ssv': display_active_scores,
        'ssmb': display_mothballed_scores,
        'lmy': manage_stylesheets,
        }
