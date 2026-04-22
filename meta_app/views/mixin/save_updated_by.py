class SaveUpdatedByMixin:

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)