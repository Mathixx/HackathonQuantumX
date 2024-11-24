
# mAIke up : Your Custom Make Up Assistant

mAIke up is a smart, AI-driven application designed to help users find the perfect makeup products and routines tailored to their preferences, skin type, and occasion. By combining cutting-edge technologies such as machine learning, natural language processing, and real-time data processing, mAIke up provides personalized product recommendations, makeup tutorials, and beauty tips. Whether you're a beginner or a beauty expert, mAIke up simplifies your beauty journey and ensures you always look your best.

mAIke up's business model centers around creating a seamless and personalized beauty experience that drives both user engagement and revenue. By leveraging advanced machine learning algorithms, the platform offers highly tailored product recommendations based on individual preferences, skin types, and occasions. This leads to higher user satisfaction and increased sales conversion. In addition to offering personalized recommendations, mAIke up generates revenue through strategic partnerships with cosmetic brands. Advertised products that are seamlessly integrated into the recommendation system allow brands to reach users in a non-intrusive, targeted manner, ensuring higher visibility and brand awareness. The platform also encourages cross-selling by suggesting complementary products during the shopping experience, driving up average order value. With access to real-time user data, mAIke up can offer brands valuable insights into customer preferences and trends, allowing for premium advertising and data-driven marketing strategies. This combination of tailored recommendations, brand partnerships, and upselling creates a sustainable and scalable business model that aligns the interests of users, brands, and mAIke up itself.

---

# How it works
This system is powered by a robust network of databases and advanced artificial intelligence, designed to seamlessly assist users through a multi-agent framework. At its core, it leverages MistralAI to create highly efficient product, user, and purchase databases. The architecture revolves around three specialized LLM agents, each with its unique role in delivering a smooth, intuitive customer experience.

The first agent specializes in data compression, optimizing the information from the databases to minimize the load and ensure efficient processing without sacrificing detail. This crucial step ensures that only the most relevant and necessary data is used throughout the system.

The heart of the system is the main agent — a sophisticated, cycle-driven model engineered to assist customers through dynamic, multi-step reasoning, fine tuned with sales data to ensure he is the best seller possible. With advanced prompt engineering and a precise framework, this agent continuously refines its responses, taking into account each piece of information gathered along the way. It is designed to understand and query data, formulate complex queries, analyze user requests, and predict what information is still missing. By heavily leveraging function calls, this agent can access and retrieve critical data from the databases, managing everything from product information to order history, and even taking action by adding products to the cart or placing orders.

Finally, the third agent acts as a powerful query engine, translating the main agent’s instructions into precise database queries using a variety of Retrieval-Augmented Generation (RAG) techniques. This agent is the key to retrieving the right data, ensuring the main agent always has the freshest and most relevant information to provide optimal service.

Together, these agents work in perfect harmony, transforming the user experience into an intelligent, responsive, and highly personalized interaction.

## DEMO

A video is available in this drive : https://drive.google.com/drive/folders/1Mz7h53gX4tGx6GNDQJNJhAiRZpWTfE1B?usp=share_link

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.



---

### Prerequisites

Ensure you have the following installed:

- [Node.js](https://nodejs.org/) (version X.X.X or later)
- [Python](https://www.python.org/) (version X.X.X or later)
- Package manager:
  - `npm` (comes with Node.js)
  - `pip` (for Python package management)

---

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Mathixx/HackathonQuantumX
cd <repository-folder>
```

#### 2. Install Dependencies

**For the Frontend:**

Navigate to the `web` folder:

```bash
cd web
npm install
```

**For the Backend:**

Navigate to the backend directory (e.g., `Manager`):

```bash
pip install -r requirements.txt
```

---

### Running the Project

#### 1. Start the Frontend

In one terminal, navigate to the `web` folder and start the frontend server:

```bash
cd web
npm start
```

The application should open automatically in your default browser. If not, visit: `http://localhost:3000`

#### 2. Start the Backend

In another terminal, navigate to the backend directory and start the server:

```bash
cd Manager
python app.py
```

The backend server should start and be accessible on `http://localhost:5000` (or another port if specified).


### Built With

- **Frontend**: [React.js](https://reactjs.org/)
- **Backend**: [Flask](https://flask.palletsprojects.com/) (or any other framework you're using)

---

### Contributing

If you would like to contribute, 

1. Fork the repository.
2. Create a branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

### Acknowledgments

- Thank you MistralAI and Quantum Black for hosting an amazing Hackathon
