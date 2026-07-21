/**
 * @fileoverview routes.constants.js - Client-Side Routing Configuration Constants
 * @module constants/routes
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Centralize all client-side page route paths.
 * 
 * Exported Constants:
 * - ROUTE_PATHS
 * 
 * Dependencies:
 * - None
 */

/**
 * Centrally defined client application route paths.
 * Consumed by navigation hooks and route guards for redirects.
 * @type {object}
 */
export const ROUTE_PATHS = {
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/forgot-password', // redirect to login or reset page
  HOME: '/'
};
