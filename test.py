import unittest
from unittest.mock import MagicMock, Mock
from bot_message_sender import BotMessageSender
from entity_manager import EntityManager
from message_processor import MessageProcessor
from user import User, UserStatus
from locations import Location

class TestLocationMovement(unittest.TestCase):
    def setUp(self):
        ms = Mock()
        self.entityManager = Mock()
        self.mp = MessageProcessor(self.entityManager, ms)


    def test_go_somewhere_changes_user_status_to_going(self):
        user = User(123)
        user.set_name('TestUser')
        user.status = UserStatus.READY
        self.entityManager.getEntityByField = MagicMock(return_value=user)

        self.mp.message(123, 'Go somewhere')

        self.assertEqual(user.status, UserStatus.GOING)

    def test_changes_user_location(self):
        user = User(123)
        user.set_name('TestUser')
        user.status = UserStatus.GOING
        self.entityManager.getEntityByField = MagicMock(return_value=user)

        self.mp.message(123, 'Forest')

        self.assertEqual(user.status, UserStatus.READY)
        self.assertEqual(user.location, Location.FOREST)


class TestDuelling(unittest.TestCase):
    def setUp(self):
        ms = Mock()
        self.entityManager = Mock()
        self.mp = MessageProcessor(self.entityManager, ms)
        user1 = User(123)
        user1.set_name('TestUser1')
        user1.location = Location.ARENA
        user1.status = UserStatus.READY
        user2 = User(321)
        user2.set_name('TestUser2')
        user2.location = Location.ARENA
        user2.status = UserStatus.READY
        self.users = {123: user1, 321: user2}

        def user_return (c, field, chat_id):
            if int(chat_id) in self.users:
                return self.users[int(chat_id)]
            else:
                return None
        self.user_return = user_return

        def getAllByField(c, field, value):
            return [self.users[user] for user in self.users if self.users[user].location == value]
        self.getAllByField = getAllByField

        self.entityManager.getEntityByField = MagicMock(side_effect=self.user_return)
        self.entityManager.getAllByField = MagicMock(side_effect=self.getAllByField)

    def test_starting_duel_with_someone(self):
        self.mp.message(123, 'Duel')

        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

    def test_starting_duel_with_no_one(self):
        self.users[321].location = Location.VILLAGE
        self.mp.message(123, 'Duel')

        self.assertEqual(self.users[123].status, UserStatus.READY)


    def test_send_invite_to_user(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(123, '321')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

    def test_send_invite_to_user_busy(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.users[321].status = UserStatus.GOING
        self.mp.message(123, '321')
        self.assertEqual(self.users[123].status, UserStatus.READY)

    def test_send_invite_to_user_other_location(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.users[321].location = Location.VILLAGE
        self.mp.message(123, '321')
        self.assertEqual(self.users[123].status, UserStatus.READY)

    def test_send_invite_to_incorrect_user(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(123, '321632')
        self.assertEqual(self.users[123].status, UserStatus.READY)

    def test_send_invite_to_user_and_start_duel(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(123, '321')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(321, 'Duel 123')
        self.assertEqual(self.users[123].status, UserStatus.DUELLING)
        self.assertEqual(self.users[321].status, UserStatus.DUELLING)

    def test_attack(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(123, '321')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(321, 'Duel 123')
        self.assertEqual(self.users[123].status, UserStatus.DUELLING)
        self.assertEqual(self.users[321].status, UserStatus.DUELLING)

        self.mp.message(123, 'Attack')
        self.assertEqual(self.users[123].status, UserStatus.DUELLING_ATTACKED)
        self.assertEqual(self.users[321].status, UserStatus.DUELLING)

        self.mp.message(321, 'Attack')
        self.assertEqual(self.users[123].status, UserStatus.DUELLING)
        self.assertEqual(self.users[321].status, UserStatus.DUELLING)

    def test_duel_end(self):
        self.mp.message(123, 'Duel')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(123, '321')
        self.assertEqual(self.users[123].status, UserStatus.STARTING_DUEL)

        self.mp.message(321, 'Duel 123')
        self.assertEqual(self.users[123].status, UserStatus.DUELLING)
        self.assertEqual(self.users[321].status, UserStatus.DUELLING)

        self.users[123].health = 1
        self.mp.message(123, 'Attack')
        self.assertEqual(self.users[123].status, UserStatus.DUELLING_ATTACKED)
        self.assertEqual(self.users[321].status, UserStatus.DUELLING)

        self.mp.message(321, 'Attack')
        self.assertEqual(self.users[123].status, UserStatus.READY)
        self.assertEqual(self.users[321].status, UserStatus.READY)

if __name__ == '__main__':
    unittest.main()
