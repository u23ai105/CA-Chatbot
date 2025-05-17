import express from 'express';
import { handleQuestion } from '../controllers/askController.js';

export const askRouter = express.Router();

askRouter.post('/', async (req, res, next) => {
  try {
    const { message } = req.body;
    const response = await handleQuestion(message);
    res.json(response);
  } catch (error) {
    next(error);
  }
});