from database import DatabaseManager
import os


class TestDatabase:
    def setup_method(self, method):
        """ Setup database """
        self.file_name = 'test.db'

        self.db_connection = DatabaseManager(self.file_name)

        self.db_connection.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })

    def teardown_method(self, method):
        """ Remove database file """
        os.remove(self.file_name)

    def test_connection(self):
        assert os.path.exists(self.file_name) == 1

    def test_table_creation(self):
        # Should be no rows.
        result = self.db_connection._execute('SELECT * FROM bookmarks')
        assert len(result.fetchall()) == 0

        # Verify column names.
        column_names = ([description[0] for description in result.description])
        assert column_names == ['id', 'title', 'url', 'notes', 'date_added']

    def test_add_row(self):
        self.db_connection.add(
            'bookmarks', {'title': 'a', 'url': 'b', 'notes': 'c', 'date_added': 'd'})

        # Should be one row.
        result = self.db_connection._execute('SELECT * FROM bookmarks')
        data = result.fetchall()

        assert len(data) == 1
        assert data == [(1, 'a', 'b', 'c', 'd')]

    def test_delete_row(self):
        self.db_connection.add(
            'bookmarks', {'title': 'a', 'url': 'b', 'notes': 'c', 'date_added': 'd'})

        # Should be one row.
        result = self.db_connection._execute('SELECT * FROM bookmarks')
        data = result.fetchall()

        assert len(data) == 1
        assert data == [(1, 'a', 'b', 'c', 'd')]

        self.db_connection.delete(
            'bookmarks', {'id': 1, 'title': 'a', 'date_added': 'd'})

        # Should be zero rows.
        result = self.db_connection._execute('SELECT * FROM bookmarks')
        assert len(result.fetchall()) == 0

    def test_select(self):
        self.db_connection.add(
            'bookmarks', {'title': 'a', 'url': 'b', 'notes': 'c', 'date_added': 'd'})
        self.db_connection.add(
            'bookmarks', {'title': 'e', 'url': 'f', 'notes': 'g', 'date_added': 'h'})

        # Should be two rows.
        result = self.db_connection._execute('SELECT * FROM bookmarks')
        data = result.fetchall()

        assert len(data) == 2
        assert data == [(1, 'a', 'b', 'c', 'd'), (2, 'e', 'f', 'g', 'h')]

        # General select usage.
        result = self.db_connection.select('bookmarks')
        data = result.fetchall()

        assert len(data) == 2
        assert data == [(1, 'a', 'b', 'c', 'd'), (2, 'e', 'f', 'g', 'h')]

        # Test criteria feature.
        result = self.db_connection.select('bookmarks', criteria={'id': 2})
        data = result.fetchall()

        assert len(data) == 1
        assert data == [(2, 'e', 'f', 'g', 'h')]

        # Test order by feature.
        # Add another bookmark where the title falls in between the titles above.
        self.db_connection.add(
            'bookmarks', {'title': 'b', 'url': 'https://hello', 'notes': 'order by test', 'date_added': 'h'})

        result = self.db_connection.select('bookmarks', order_by='title')
        data = result.fetchall()

        assert len(data) == 3
        assert data == [(1, 'a', 'b', 'c', 'd'), (3, 'b', 'https://hello', 'order by test', 'h'), (2, 'e', 'f', 'g', 'h')]

        # Test criteria and order by in the same query.
        result = self.db_connection.select('bookmarks', criteria={'id': 3})
        data = result.fetchall()

        assert len(data) == 1
        assert data == [(3, 'b', 'https://hello', 'order by test', 'h')]

    def test_drop_table(self):
        # Should be no rows.
        result = self.db_connection._execute('SELECT * FROM bookmarks')
        assert len(result.fetchall()) == 0

        # Verify column names.
        column_names = ([description[0] for description in result.description])
        assert column_names == ['id', 'title', 'url', 'notes', 'date_added']

        self.db_connection.drop_table('bookmarks')
        result = self.db_connection._execute("SELECT name FROM sqlite_master WHERE type='bookmarks' ORDER BY name;")
        assert len(result.fetchall()) == 0
