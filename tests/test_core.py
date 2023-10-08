import unittest

from erlanglib import factorial, calculate_erlangs, \
     erlang_b, required_channels, calculate_erlangs_from_blocking, \
     calls_per_second_from_erlangs,call_duration_from_erlangs, \
     erlang_c, service_level, average_speed_of_answer, \
     immediate_answer_percentage, occupancy, required_agents


class TestErlangLib(unittest.TestCase):

    def test_factorial(self):

        # factorial 0 = 1 .... there are positive values <0
        self.assertEqual(factorial(0), 1)

        # factorial 1 = 1
        self.assertEqual(factorial(1), 1)

        # factorial 2 = 2
        self.assertEqual(factorial(2), 2)

        # factorial 3 = 6
        self.assertEqual(factorial(3), 6)

        # factorial 4 = 24
        self.assertEqual(factorial(4), 24)

    def test_calculate_erlangs(self):

        # For a call duration of 60 seconds (1 minute) and 1 call per second
        # Erlangs = 1/60 * 3600 = 60
        self.assertEqual(calculate_erlangs(60, 1), 60)

        # For a call duration of 120 seconds (2 minutes) and 0.5 calls per second
        # Erlangs = 2/60 * 0.5 * 3600 = 60
        self.assertEqual(calculate_erlangs(120, 0.5), 60)

        # For a call duration of 30 seconds and 2 calls per second
        # Erlangs = 0.5/60 * 2 * 3600 = 60
        self.assertEqual(calculate_erlangs(30, 2), 60)

    def test_calls_per_second_from_erlangs(self):

        # Given Erlangs of 48,000 and a call duration of 8 minutes (480 seconds) = 100 calls per second
        self.assertAlmostEqual(calls_per_second_from_erlangs(48000, 480), 100, places=2)

    def test_call_duration_from_erlangs(self):

        # Given Erlangs of 48,000 and 100 calls per second = 480 seconds call duration
        self.assertAlmostEqual(call_duration_from_erlangs(48000, 100), 480, places=2)

    def test_erlang_b(self):

        # For 10 channels (N) and offered load (A) 5 Erlangs =  0.018384570336648136 = 1.8%
        self.assertAlmostEqual(erlang_b(10, 5), 0.018384, places=4)

        # For 10 channels (N) and offered load (A) 20 Erlangs =  0.5379631686320729 = 53.8%
        self.assertAlmostEqual(erlang_b(10, 20), 0.53796, places=4)

    def test_required_channels(self):

        A = 5
        target_blocking = 0.010
        # For an offered load (A) 5 Erlangs and a targeted blocking probability (B) of 1% = 11 channels needed
        self.assertTrue(required_channels(A, target_blocking), 11)

        A = 10
        target_blocking = 0.010
        # For an offered load (A) 10 Erlangs and a targeted blocking probability (B) of 1% = 18 channels needed
        self.assertEqual(required_channels(A, target_blocking), 18)

    def test_calculate_erlangs_from_blocking(self):

        # For 10 channels and target blocking probability 0.0184 (1.84%) = 5
        self.assertAlmostEqual(calculate_erlangs_from_blocking(10, 0.0184), 5, places=1)

        # For 10 channels and target blocking probability 0.53796 (53.8%) = 20
        self.assertAlmostEqual(calculate_erlangs_from_blocking(10, 0.53796), 20, places=1)

    def test_erlang_c(self):

        # For 12 servers (N) and offered load (A) 10 Erlangs the probability a call will wait = 0.2853 = 28.53 %
        self.assertAlmostEqual(erlang_c(11, 10), 0.6821, places=4)

        # For 14 servers (N) and offered load (A) 10 Erlangs the probability a call will wait = 0.2853 = 28.53 %
        self.assertAlmostEqual(erlang_c(14, 10), 0.1741, places=4)

    def test_service_level(self):

        N = 11  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        target_time_seconds = 20
        AHT_seconds = 180
        expected_service_level = 0.390
        self.assertAlmostEqual(service_level(N, A, Pw, target_time_seconds, AHT_seconds), expected_service_level,
                               places=2)

        N = 12  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        target_time_seconds = 20
        AHT_seconds = 180
        expected_service_level = 0.640
        self.assertAlmostEqual(service_level(N, A, Pw, target_time_seconds, AHT_seconds), expected_service_level,
                               places=2)

        N = 14  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        target_time_seconds = 20
        AHT_seconds = 180
        expected_service_level =  0.888350
        self.assertAlmostEqual(service_level(N, A, Pw, target_time_seconds, AHT_seconds), expected_service_level,
                               places=2)

    def test_average_speed_of_answer(self):

        N = 14  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        average_handling_time = 180

        expected_asa = 7.83593
        self.assertAlmostEqual(average_speed_of_answer(N, A, Pw, average_handling_time), expected_asa, places=2)

    def test_immediate_answer_percentage(self):

        N = 14  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        print(Pw)

        expected_percentage = 82.586
        self.assertAlmostEqual(immediate_answer_percentage(Pw), expected_percentage, places=2)

    def test_occupancy(self):

        A = 10  # Traffic in Erlangs
        N = 14  # Number of agents

        expected_occupancy = 71.4285
        self.assertAlmostEqual(occupancy(A, N), expected_occupancy, places=2)

    def test_required_agents(self):

        # For raw agents = 14 and shrinkage = 30%
        # required agents = 14 / (1 - 0.30) = 20 agents
        self.assertEqual(required_agents(14, 30), 20)

        # For raw agents = 50 and shrinkage = 20%
        # required agents = 50 / (1 - 0.20) = 62.5 which rounds to 63
        self.assertEqual(required_agents(50, 20), 63)


if __name__ == '__main__':
    unittest.main()
