package jdg.digital.forexfrontend.security;


import jakarta.servlet.http.HttpSessionEvent;
import jakarta.servlet.http.HttpSessionListener;

/**
 * {@link HttpSessionListener} that updates a {@link SessionRepository} when sessions are created and destroyed.
 */
public class SessionRepositoryListener implements HttpSessionListener {

    private final SessionRepository sessionRepository;

    public SessionRepositoryListener(SessionRepository sessionRepository) {
        this.sessionRepository = sessionRepository;
    }

    @Override
    public void sessionCreated(HttpSessionEvent se) {
        sessionRepository.add(se.getSession());
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        sessionRepository.remove(se.getSession());
    }
}
