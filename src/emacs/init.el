;; Disable backup files.
(setq make-backup-files nil)
(setq auto-save-default nil)

;; Set forward/backward jump for CTRL+cursor keys.
(global-set-key "\M-[1;5C"    'forward-word)
(global-set-key "\M-[1;5D"    'backward-word)
(global-set-key "\M-[1;5A"    'backward-paragraph)
(global-set-key "\M-[1;5B"    'forward-paragraph)

;; Shor row and column.
(line-number-mode t)
(column-number-mode t)

;; Show trailing white spaces
(setq-default show-trailing-whitespace t)

;; Disable tabs by default
(setq-default indent-tabs-mode nil)

;; For google-c-style
(add-to-list 'load-path user-emacs-directory)
(add-hook 'c-mode-common-hook
          '(lambda ()
             (require 'google-c-style)
             (google-set-c-style)
             (google-make-newline-indent)))

;; Set .h file to c++-mode.
(add-to-list 'auto-mode-alist '("\\.h$" . c++-mode))
