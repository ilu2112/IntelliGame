import java.io.*;


public class AverageTheGame {
	
	private static BufferedReader reader;
	

	private int numberOfTurns = 2;
	private long timePerTurn = 3000;	// milliseconds

	private int numberOfPlayers;
	private int[] score;
	private int[] guess;


	private AverageTheGame(int numberOfPlayers) {
		this.numberOfPlayers = numberOfPlayers;
		score = new int[numberOfPlayers];
		guess = new int[numberOfPlayers];
	}


	private void run() {
		// for each turn
		for (int turn = 1; turn <= numberOfTurns; turn++) {
			// clear player's guesses
			for (int i = 0; i < numberOfPlayers; i++) {
				guess[i] = -1;
			}

			// start time counter
			long startTurnTime = System.currentTimeMillis();
			
			// start the turn
			for (int i = 0; i < numberOfPlayers; i++) {
				System.out.println("bot " + (i + 1) + ":turn");
			}

			// while we have time
			while (System.currentTimeMillis() - startTurnTime < timePerTurn) {
				// answer queries
				try {
					if (reader.ready()) {
						String query = reader.readLine();
						dispatchQuery(query);
					}
				} catch (IOException e) {
					System.err.print(e);
				}
			}

			// in the end of the turn - calculate the winner
			calculateWinner();
		}
		
		// close bots
		for (int i = 0; i < numberOfPlayers; i++) {
			System.out.println("bot " + (i + 1) + ":end");
		}

		// int the end of the game - pass scores
		passScores();
		
		// wait for termination
		try {
			while (!reader.ready()) {
			}
			reader.readLine();
		} catch (IOException e) {
			System.err.print(e);
		}
	}


	private void dispatchQuery(String query) {
		int bot = new Integer(query.split(":")[0].split(" ")[1].trim());
		int gue = new Integer(query.split(":")[1].trim());
		guess[bot] = gue;
	}


	private void sendMessageToPlayer(int player, String message) {
		sendMessageToSandbox("Player " + player + " :" + message);
	}


	private void sendMessageToSandbox(String message) {
		System.out.println(message);
	}


	private void calculateWinner() {
		// calculate average number
		double sumOfGuesses = 0.0;
		double quantityOfGuesses = 0.0;
		for (int i = 0; i < numberOfPlayers; i++) {
			if (guess[i] != -1) {
				sumOfGuesses += (double) guess[i];
				quantityOfGuesses += 1.0;
			}
		}
		double average = 0.66666667 * sumOfGuesses / quantityOfGuesses;
		// choose the winner
		int winner = -1;
		int numberOfWinners = 0;
		for (int i = 0; i < numberOfPlayers; i++) {
			if (guess[i] != -1) {
				if (winner == -1 || Math.abs(average - guess[winner]) > Math.abs(average - guess[i])) {
					winner = i;
					numberOfWinners = 1;
				} else if (winner != -1 && Math.abs(average - guess[winner]) == Math.abs(average - guess[i])) {
					numberOfWinners += 1;
				}
			}
		}
		if (winner != -1 && numberOfWinners == 1) {
			score[winner] += 1;
		}
	}


	private void passScores() {
		System.out.println("results begin");
		System.out.flush();
		for (int i = 0; i < numberOfPlayers; i++) {
			System.out.println(score[i] + " -");
			System.out.flush();
		}
		System.out.println("results end");
		System.out.flush();
	}


	public static void main(String[] args) {
		// create reader and writer
		reader = new BufferedReader(new InputStreamReader(System.in));
		// read initial data
		try {
			// number of players
			String line = reader.readLine();
			int numberOfPlayers = new Integer(line.split(" ")[1]);
			// ignore time left
			reader.readLine();
			// run the game
			new AverageTheGame(numberOfPlayers).run();
		} catch (IOException e) {
			System.err.println(e);
		}
	}
}