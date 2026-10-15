declare global {
  namespace App {
    interface Locals {
      user: {
        id: string;
        nombre: string;
        rol: 'operador' | 'administrador';
      } | null;
    }
  }
}

export {};
