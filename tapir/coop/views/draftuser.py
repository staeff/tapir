from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET

from tapir.coop import pdfs
from tapir.coop.forms import (
    DraftUserForm,
    DraftUserRegisterForm,
)
from tapir.coop.models import (
    DraftUser,
    ShareOwner,
    ShareOwnership,
)
from tapir.utils.models import copy_user_info


class DraftUserViewMixin:
    model = DraftUser
    form_class = DraftUserForm


class DraftUserListView(PermissionRequiredMixin, DraftUserViewMixin, generic.ListView):
    permission_required = "coop.manage"


class DraftUserCreateView(
    PermissionRequiredMixin, DraftUserViewMixin, generic.CreateView
):
    permission_required = "coop.manage"


class DraftUserRegisterView(DraftUserViewMixin, generic.CreateView):
    template_name = "coop/draftuser_register_form.html"
    form_class = DraftUserRegisterForm
    success_url = "/coop/user/draft/register/confirm"


class DraftUserConfirmRegistrationView(DraftUserViewMixin, generic.TemplateView):
    template_name = "coop/draftuser_confirm_registration.html"


class DraftUserUpdateView(
    PermissionRequiredMixin, DraftUserViewMixin, generic.UpdateView
):
    permission_required = "coop.manage"


class DraftUserDetailView(
    PermissionRequiredMixin, DraftUserViewMixin, generic.DetailView
):
    permission_required = "coop.manage"


class DraftUserDeleteView(
    PermissionRequiredMixin, DraftUserViewMixin, generic.DeleteView
):
    permission_required = "coop.manage"
    success_url = reverse_lazy("coop:draftuser_list")


@require_GET
@permission_required("coop.manage")
def draftuser_membership_agreement(request, pk):
    draft_user = get_object_or_404(DraftUser, pk=pk)
    filename = "Beteiligungserklärung %s %s.pdf" % (
        draft_user.first_name,
        draft_user.last_name,
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="{}"'.format(filename)
    response.write(pdfs.get_membership_agreement_pdf(draft_user).write_pdf())
    return response


@require_POST
@csrf_protect
@permission_required("coop.manage")
def mark_signed_membership_agreement(request, pk):
    u = DraftUser.objects.get(pk=pk)
    u.signed_membership_agreement = True
    u.save()

    return redirect(u)


@require_POST
@csrf_protect
@permission_required("coop.manage")
def mark_attended_welcome_session(request, pk):
    u = DraftUser.objects.get(pk=pk)
    u.attended_welcome_session = True
    u.save()

    return redirect(u)


@require_POST
@csrf_protect
@permission_required("coop.manage")
def register_draftuser_payment(request, pk):
    draft = get_object_or_404(DraftUser, pk=pk)
    draft.paid_membership_fee = True
    draft.save()
    return redirect(draft.get_absolute_url())


@require_POST
@csrf_protect
@permission_required("coop.manage")
def create_share_owner_from_draftuser(request, pk):
    # For now, we don't create users for our new members yet but only ShareOwners. Later, this will be used for
    # investing members

    draft = DraftUser.objects.get(pk=pk)
    if not draft.signed_membership_agreement:
        # TODO(Leon Handreke): Error message
        return redirect(draft)

    if draft.num_shares < 0:
        raise Exception(
            "Trying to create a share owner from a draft user without shares"
        )

    with transaction.atomic():
        share_owner = ShareOwner.objects.create(
            is_company=False,
            is_investing=draft.is_investing,
            from_startnext=draft.from_startnext,
            ratenzahlung=draft.ratenzahlung,
            attended_welcome_session=draft.attended_welcome_session,
            paid_membership_fee=draft.paid_membership_fee,
        )

        copy_user_info(draft, share_owner)
        share_owner.save()

        for _ in range(0, draft.num_shares):
            ShareOwnership.objects.create(
                owner=share_owner,
                start_date=date.today(),
            )

        draft.delete()

    return redirect(share_owner.get_absolute_url())
