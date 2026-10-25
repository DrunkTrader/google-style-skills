import type {User} from './user';

export function displayName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}
