package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;

import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import cn.edu.tsinghua.thss.popcorn.AboutInfoActivity;
import cn.edu.tsinghua.thss.popcorn.ChangePasswordActivity;
import cn.edu.tsinghua.thss.popcorn.FeedBackActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.RecordListActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;


/**
 * @author wenqingfu
 * @email thssvince@163.com
 */

public class MineFragment extends Fragment {

    private View mineView;

    @ViewInject(R.id.mine_name)
    private TextView myName;

    @ViewInject(R.id.mine_username)
    private TextView myUserName;

    @OnClick(R.id.change_password)
    private void onChangePsdClick(View v) {
        Intent intent = new Intent(getActivity(), ChangePasswordActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.feed_back)
    private void onFeedBackClick(View v) {
        Intent intent = new Intent(getActivity(), FeedBackActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.about_info)
    private void onAboutInfoClick(View v) {
        Intent intent = new Intent(getActivity(), AboutInfoActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.log_out)
    private void onLogOutClick(View v){
        getActivity().finish();
    }

    @Override
    public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
        super.onCreateView(inflater, container, savedInstanceState);

        if(mineView==null){
            mineView=inflater.inflate(R.layout.activity_tab_mine, null);
        }

        ViewGroup parent = (ViewGroup) mineView.getParent();
        if (parent != null) {
            parent.removeView(mineView);
        }
        ViewUtils.inject(this, mineView);

        setMineView();

        return mineView;
    }

    private void setMineView(){
        myUserName.setText("用户名："+Config.DEBUG_USERNAME);
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState){
        super.onActivityCreated(savedInstanceState);
    }
}
