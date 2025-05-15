import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchArticles = async (query) => {
  try {
    const response = await api.get(`/search/?q=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    console.error('Error searching articles:', error);
    throw error;
  }
};

export const getArticleDetails = async (pageId) => {
  try {
    const response = await api.get(`/articles/detail/${pageId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting article details:', error);
    throw error;
  }
};

export const saveArticle = async (article) => {
  try {
    const response = await api.post('/articles/', article);
    return response.data;
  } catch (error) {
    console.error('Error saving article:', error);
    throw error;
  }
};

export const getSavedArticles = async (skip = 0, limit = 10) => {
  try {
    const response = await api.get(`/articles/?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error getting saved articles:', error);
    throw error;
  }
};

export const updateArticle = async (articleId, updateData) => {
  try {
    const response = await api.patch(`/articles/${articleId}`, updateData);
    return response.data;
  } catch (error) {
    console.error('Error updating article:', error);
    throw error;
  }
};

export const deleteArticle = async (articleId) => {
  try {
    const response = await api.delete(`/articles/${articleId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting article:', error);
    throw error;
  }
};

export default {
  searchArticles,
  getArticleDetails,
  saveArticle,
  getSavedArticles,
  deleteArticle,
  updateArticle,
};